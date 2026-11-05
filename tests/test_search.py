from askcode.search import search_symbols


def test_search_finds_class():
    report = {
        "python_analysis": [{
            "file": "app.py",
            "classes": [{
                "name": "ArticleController",
                "line": 10,
                "methods": [],
            }],
            "functions": [],
        }],
        "php_analysis": [],
    }

    results = search_symbols(report, "ArticleController")

    assert len(results) == 1
    assert results[0]["type"] == "class"
    assert results[0]["line"] == 10


def test_search_finds_method():
    report = {
        "python_analysis": [{
            "file": "app.py",
            "classes": [{
                "name": "ArticleController",
                "line": 10,
                "methods": [{
                    "name": "importArticles",
                    "line": 15,
                }],
            }],
            "functions": [],
        }],
        "php_analysis": [],
    }

    results = search_symbols(report, "importArticles")

    assert len(results) == 1
    assert results[0]["type"] == "method"
    assert results[0]["class"] == "ArticleController"
    assert results[0]["line"] == 15


def test_search_is_case_insensitive():
    report = {
        "python_analysis": [{
            "file": "app.py",
            "classes": [{
                "name": "ArticleController",
                "line": 10,
                "methods": [],
            }],
            "functions": [],
        }],
        "php_analysis": [],
    }

    results = search_symbols(report, "articlecontroller")

    assert len(results) == 1