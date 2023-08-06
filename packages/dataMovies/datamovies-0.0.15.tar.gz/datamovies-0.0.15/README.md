
# Table of Contents

1.  [Description 😊](#org660b55e)
    1.  [Maintainers 👨👩👧👦](#orged9041f)
2.  [Prerequisites 🏁](#org40169ba)
3.  [Installation ✅](#orgbdd3be0)
4.  [Usage 😁](#org0d50776)
5.  [Run tests ⚙](#org5f6690e)
    1.  [Clone the repository](#org40cf692)
    2.  [run unit tests](#org397d5e4)



<a id="org660b55e"></a>

# Description 😊

DataMovies is a data-science focused library that allows you to request movies/series dataset via ImDb&rsquo;s API.

Available for now:

-   search all users reviews for a specific movie
-   search all ratings distributions for a specific movie
    -   statistic by ratings
    -   ratings per age range for man
    -   ratings per age range for woman
    -   ratings per age range for all


<a id="orged9041f"></a>

## Maintainers 👨👩👧👦

-   [@rizerkrof](https://github.com/rizerkrof)
-   [@Zuwhity](https://github.com/Zuwhity)
-   [@HaozGU](https://github.com/HaozGU)


<a id="org40169ba"></a>

# Prerequisites 🏁

-   Python >= 3.8
-   pip


<a id="orgbdd3be0"></a>

# Installation ✅

From [official repository](https://pypi.org/project/dataMovies/):

    pip install dataMovies


<a id="org0d50776"></a>

# Usage 😁

Look at the [example](https://github.com/rizerkrof/libray-dataMovies/tree/main/example) to know more about the use. Do not forget to check the [documentation](https://rizerkrof.github.io/libray-dataMovies/dataMovies/dataMovies.html) to see all features information!


<a id="org5f6690e"></a>

# Run tests ⚙


<a id="org40cf692"></a>

## Clone the repository

    git clone https://github.com/rizerkrof/libray-dataMovies.git
    cd libray-dataMovies


<a id="org397d5e4"></a>

## run unit tests

    python3 -m unittest discover --top-level-directory=. --start-directory=./tests/tests_dataMovies/

