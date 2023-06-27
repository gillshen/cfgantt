import re
import datetime
import json
import dataclasses

import jinja2

__all__ = ["Task", "parse", "parse_file", "make_html"]


class ParserError(Exception):
    pass


class MissingDataError(Exception):
    pass


class DateError(ParserError):
    pass


@dataclasses.dataclass
class Task:
    name: str
    start: str
    end: str
    custom_class: str = None
    id: str = None
    progress: int = 0
    dependencies: str = ""


@dataclasses.dataclass
class Plan:
    title: str = ""
    state: str = ""
    goals: str = ""
    tasks: list[Task] = dataclasses.field(default_factory=list)
    state_label: str = "现有硬性条件"
    goals_label: str = "申请季目标"

    def stringfy(self) -> "Plan":
        tasks = map(dataclasses.asdict, self.tasks)
        tasks_string = json.dumps(list(tasks), ensure_ascii=False, indent=2)
        return dataclasses.replace(self, tasks=tasks_string)


def _compile(keyword):
    return re.compile(rf"^\s*{keyword}\s*[:：](.*)$", flags=re.IGNORECASE)


TITLE = _compile("title")
STATE = _compile("state")
GOALS = _compile("goals")
STATE_LABEL = _compile(r"state\s*label")
GOALS_LABEL = _compile(r"goals\s*label")

TASK = _compile("task")
DATE = _compile("date")
WHO = _compile("who")
ID = _compile("id")
PROGRESS = _compile("progress")
DEPENDENCIES = _compile("dependencies")


def parse_file(filepath: str, encoding="utf-8") -> Plan:
    with open(filepath, encoding=encoding) as f:
        return parse(f.read())


def parse(text: str) -> Plan:
    plan = Plan()
    data = None

    for line in text.splitlines():
        line = re.sub(r"\s+", " ", line).strip()

        if not line:
            continue

        if title := _extract(TITLE, line):
            plan.title = title
        elif state := _extract(STATE, line):
            plan.state = state
        elif goals := _extract(GOALS, line):
            plan.goals = goals
        elif state_label := _extract(STATE_LABEL, line):
            plan.state_label = state_label
        elif goals_label := _extract(GOALS_LABEL, line):
            plan.goals_label = goals_label

        elif task_name := _extract(TASK, line):
            if data is not None:
                plan.tasks.append(_create_task(data))
            data = {"name": task_name}

        elif task_date := _extract(DATE, line):
            try:
                start, end = re.split(r"\s+", task_date)
            except ValueError:
                start = end = task_date
            data["start"] = _parse_date(start)
            data["end"] = _parse_date(end, end=True)

        elif who := _extract(WHO, line):
            data["custom_class"] = _to_custom_class(who)
        elif task_id := _extract(ID, line):
            data["id"] = task_id

        elif progress := _extract(PROGRESS, line):
            data["progress"] = progress
        elif dependencies := _extract(DEPENDENCIES, line):
            data["dependencies"] = dependencies

        else:
            print(f"unparsed: {line!r}")

    if data is not None:
        plan.tasks.append(_create_task(data))

    if not plan.tasks:
        raise MissingDataError("No tasks to plot")

    return plan


def _extract(pattern: re.Pattern, text: str) -> str | None:
    if mo := pattern.match(text):
        return mo.group(1).strip()


def _create_task(data: dict) -> Task:
    try:
        return Task(**data)
    except TypeError:
        raise MissingDataError(data)


def _parse_date(date_str: str, end=False) -> str:
    # Convert a partial with only year and month to a full date
    try:
        mo = re.match(r"^(\d{4})-(\d\d?)(?:-(\d\d?))?", date_str)
        yyyy, mm, dd = mo.groups()
    except AttributeError as e:
        raise DateError(date_str) from e

    year = int(yyyy)
    month = int(mm)
    try:
        if dd:
            return str(datetime.date(year, month, int(dd)))
        if not end:
            return str(datetime.date(year, month, 1))
        else:
            # return the last day of the month
            next_month = datetime.date(year, month, 28) + datetime.timedelta(days=4)
            last_day = next_month - datetime.timedelta(days=next_month.day)
            return str(last_day)

    except ValueError as e:
        raise DateError(date_str) from e


def _to_custom_class(who: str) -> str:
    if who == "s":
        return "student"
    if who == "w":
        return "wenan"
    if who == "g":
        return "guwen"
    raise ParserError(f'Invalid {who=!r}. Should be "s", "w", or "g".')


ENVIRONMENT = jinja2.Environment(
    variable_start_string="/*",
    variable_end_string="*/",
    trim_blocks=False,
    keep_trailing_newline=True,
)


def make_html(fp, plan: Plan):
    with open("assets/template.html", encoding="utf-8") as template_file:
        template_str = template_file.read()
    template = ENVIRONMENT.from_string(template_str)

    with open("assets/frappe-gantt.min.js", encoding="utf-8") as frappe_js_file:
        frappe_js = frappe_js_file.read()

    with open("assets/frappe-gantt.min.css", encoding="utf-8") as frappe_css_file:
        frappe_css = frappe_css_file.read()

    with open("assets/chart.css", encoding="utf-8") as css_file:
        css = css_file.read()

    html = template.render(
        frappe_js=frappe_js, frappe_css=frappe_css, css=css, plan=plan.stringfy()
    )
    fp.write(html)


def _test():
    with open("__chart.js", mode="w", encoding="utf-8") as f:
        make_html(f, plan=parse_file("sample/sample.txt"))


if __name__ == "__main__":
    _test()
