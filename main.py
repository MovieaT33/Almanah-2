import json
import random
import sys
from enum import StrEnum
from typing import NoReturn


class Colors(StrEnum):
    RED = "31m"
    GREEN = "32m"
    RESET = "0m"

    def __str__(self) -> str:
        return f"\033[{self.value}"


JSON_DIR: str = "json"


def parse_text(text: str, colors: dict[str, str]) -> str:
    for color_name, color_code in colors.items():
        text = text.replace(f"<{color_name}>", f"\033[{color_code}")
    return text


def print_title(title: str, colors: dict[str, str]) -> None:
    print(parse_text(title, colors))


def print_separation(
    separations: list[dict], sep_id: int, colors: dict[str, str],
) -> None | NoReturn:
    for sep in separations:
        if sep["id"] == sep_id:
            print(parse_text(sep["title"], colors))
            return None
    raise ValueError(f"Separation with id {sep_id} not found")


def print_separations(
    separations: list[dict], sep_ids: list[int], colors: dict[str, str],
) -> None:
    for sep_id in sep_ids:
        print_separation(separations, sep_id, colors)


def print_question(
    questions: list[dict],
    q_id: int,
    separations: list[dict],
    colors: dict[str, str],
) -> None | NoReturn:
    for q in questions:
        if q["id"] == q_id:
            print_separations(separations, q.get("separations", []), colors)
            print(parse_text(q["text"], colors))
            return None
    raise ValueError(f"Question with id {q_id} not found")


def print_answer(
    questions: list[dict],
    q_id: int,
    colors: dict[str, str],
) -> None | NoReturn:
    for q in questions:
        if q["id"] == q_id:
            print(parse_text(q["answer"], colors))
            return None
    raise ValueError(f"Answer for question with id {q_id} not found")


def clear_console() -> None:
    print("\033[H\033[J", end="")


def study(
    colors: dict[str, str],
    title: str,
    separations: list[dict],
    questions: list[dict],
    shuffle: bool = True,
) -> None:
    print_title(title, colors)

    shuffled_questions: list[dict] = questions.copy()
    if shuffle:
        random.shuffle(shuffled_questions)

    for q in shuffled_questions:
        print_question(questions, q["id"], separations, colors)
        input("Your answer: ")

        print("Correct answer: ", end="")
        print_answer(questions, q["id"], colors)

        input("Press Enter to continue...")
        clear_console()


# def test(quiz: dict) -> None:
#     ...


def main(quiz_filename: str) -> None:
    # 1. Load quiz from JSON file
    print(f"Quiz file: '{quiz_filename}'")
    print("Loading quiz...", end="")
    try:
        with open(quiz_filename, "r", encoding="utf-8") as file:
            quiz: dict = json.load(file)
    except OSError as exc:
        print(f" {Colors.RED}Error{Colors.RESET}: {exc}")
        return

    print(f" {Colors.GREEN}OK{Colors.RESET}")

    # 2. Load quiz data
    print("Loading quiz data...", end="")
    colors: dict[str, str] = quiz.get("colors", {})
    title: str = quiz.get("title", "Untitled Quiz")
    separations: list[dict] = quiz.get("separations", [])
    try:
        questions: list[dict] = quiz["questions"]
    except KeyError:
        print(f" {Colors.RED}Error{Colors.RESET}: No questions found in quiz "
              "data")
        return

    print(f" {Colors.GREEN}OK{Colors.RESET}")
    clear_console()

    # 3.
    study(colors, title, separations, questions)


if __name__ == "__main__":
    main(f"{JSON_DIR}/{sys.argv[1]}.json")
