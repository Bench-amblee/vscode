import json
import string
import sys

import streamlit as st

VERSION = "0.3.3"

st.set_page_config(
    page_title="Wordle Solver",
    page_icon="favicon.png",
    menu_items={
        "About": f"Wordle Solver v{VERSION}  "
        f"\nApp contact: [Siddhant Sadangi](mailto:siddhant.sadangi@gmail.com)",
        "Report a Bug": "https://github.com/SiddhantSadangi/WordleSolver/issues/new",
        "Get help": None,
    },
)

# ---------- SIDEBAR ----------
#with open("sidebar.html", "r", encoding="UTF-8") as sidebar_file:
    #idebar_html = sidebar_file.read().replace("{VERSION}", VERSION)

with st.sidebar:
    st.header("Instructions")
    st.info(
        "1. Visit any wordle app/site (for example, the [original](https://www.nytimes.com/games/wordle/index.html))\n"
        "2. Enter the length of the word\n"
        "3. Enter the word suggested by the solver in the wordle app\n"
        "4. Enter the result of the attempt as a sequence of colors: b (black), y (yellow), or g (green)\n"
        "5. Repeat steps 3 and 4 till you find a solution"
    )
    #st.image(
        #"example.png",
        #caption="For example, enter 'ybgyy' if the result looks like this",
    #st.components.v1.html(sidebar_html, height=450)

# ---------- HEADER ----------
st.title("Welcome to Wordle Solver!")
filtered_words = ['aaaaa','bbbbb','ccccc']

# ---------- RUN THE LOOP ----------

i = 1

try:
    while filtered_words:
        word = sorted(filtered_words.items(), key=lambda item: item[1], reverse=True)[
            0
        ][0]

        lcol, rcol = st.columns(2)
        lcol.subheader(f"Attempt: {i}")
        rcol.subheader(f"Enter: {word.upper()}")

        result = st.text_input(
            "Enter result colors",
            placeholder="b" * length,
            max_chars=length,
            key=i,
            help="Enter the result for each letter in the format: Black: b | Yellow: y | Green: g",
        ).lower()

        # Result validation
        if len(result) != length:
            st.warning(
                f"Result string must be {length} letters long. Please correct results"
            )
            sys.exit()

        elif any(letter for letter in result if letter not in ("b", "y", "g")):
            st.warning(
                "Valid letters are b (black), y (yellow), or g (green). Please correct results"
            )
            sys.exit()

        # Solved
        if result == "g" * length:
            st.success(f"Solved in {i} attempts!")
            st.balloons()
            break

        correct, exclude, include = {}, {}, {}

        for idx, res in enumerate(result):
            if res == "b":
                exclude[idx] = word[idx]
            elif res == "g":
                correct[idx] = word[idx]
            else:
                include[idx] = word[idx]

        only_excluded = {
            letter for letter in exclude.values() if letter not in correct.values()
        }

        # Removing words which contain any of the only excluded letters
        filtered_words = {
            k: v for k, v in filtered_words.items() if not only_excluded.intersection(k)
        }

        # Removing words which contain excluded letters in excluded positions
        tmp_dict = filtered_words.copy()
        if exclude:
            for w in filtered_words:
                for idx, l in exclude.items():
                    if w[idx] == l:
                        del tmp_dict[w]
                        break

        filtered_words = tmp_dict.copy()

        # Removing words which don't contain correct letters in correct position
        tmp_dict = filtered_words.copy()

        if correct:
            for w in filtered_words:
                for idx, l in correct.items():
                    if w[idx] != l:
                        del tmp_dict[w]
                        break

        filtered_words = tmp_dict.copy()

        # Removing words which don't contain all the included letters
        tmp_dict = filtered_words.copy()

        if include:
            for w in filtered_words:
                if any(letter for letter in include.values() if letter not in w):
                    del tmp_dict[w]
                else:
                    # Removing words which contain included letters in excluded positions
                    for idx, l in include.items():
                        if w[idx] == l:
                            del tmp_dict[w]
                            break

        filtered_words = tmp_dict.copy()

        i += 1

    else:
        st.error(
            "We cannot seem to find a solution. Are you sure the results entered are correct?"
        )

except TypeError:
    st.warning(
        "Waiting for input. Please refresh the page if you feel something is wrong."
    )

except SystemExit:
    pass