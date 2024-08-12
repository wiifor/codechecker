import argparse
import json
import os

"""
Dict used to link documentation on the different warning we can have with
eslint and its plugins.
"""
DOC_ESLINT_PLUGINS = {
        "@angular-eslint": {
            "doc_url": "https://github.com/angular-eslint/angular-eslint/tree/main/packages/eslint-plugin/docs/rules",
            "format": ".md"
        },
        "@angular-eslint/template/": {
            "doc_url": "https://github.com/angular-eslint/angular-eslint/tree/main/packages/eslint-plugin-template/docs/rules",
            "format": ".md"
        },
        "@typescript-eslint": {
            "doc_url": "https://typescript-eslint.io/rules",
            "format": ""
        },
        "eslint": {
            "doc_url": "https://eslint.org/docs/latest/rules",
            "format": ""
        },
        "import": {
            "doc_url": "https://github.com/import-js/eslint-plugin-import/blob/main/docs/rules",
            "format": ".md"
        },
        "unused-imports": {
            "doc_url": "https://github.com/sweepline/eslint-plugin-unused-imports/blob/master/docs/rules",
            "format": ".md"
        },
        "tsdoc": {
            "doc_url": "https://tsdoc.org/pages/packages/eslint-plugin-tsdoc",
            "format": ""
        },
    }

RULES_EXTENDS_ESLINT_PLUGINS = {
    "@angular-eslint/template/recommended": {
        "@angular-eslint/template/banana-in-box": ["doc_url:https://github.com/angular-eslint/angular-eslint/blob/main/packages/eslint-plugin-template/docs/rules/banana-in-box.md", "severity:HIGH"],
        "@angular-eslint/template/eqeqeq": ["doc_url:https://github.com/angular-eslint/angular-eslint/blob/main/packages/eslint-plugin-template/docs/rules/eqeqeq.md", "severity:HIGH"],
        "@angular-eslint/template/no-negated-async": ["doc_url:https://github.com/angular-eslint/angular-eslint/blob/main/packages/eslint-plugin-template/docs/rules/no-negated-async.md", "severity:HIGH"]
    }
}

def cli_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--config-file',
        required=True,
        nargs='+',
        help='Path to the config file(s) which will be inserted the checker '
             'documentation URLs.')

    parser.add_argument(
        '--label-file',
        required=True,
        help='Path to the label file which will be inserted the checker '
             'documentation URLs.')

    return parser.parse_args()


def get_severity(label):
    if label == "off":
        return None
    else:
        return "HIGH" if label == "error" else "LOW"


def main():
    args = cli_args()

    file_to_open = args.config_file
    file_to_write = args.label_file
    labels = {"eslint": ["doc_url:https://eslint.org/docs/latest/rules/", "severity:MEDIUM"]}
    for file in file_to_open:
        f = open(file)
        conf = json.load(f)

        for ov in (conf["overrides"]):
            rules = ov["rules"]
            if rules:
                for i in range(len(rules)):
                    checker_name = list(rules.keys())[i]
                    checker_splitted = checker_name.rsplit("/", 1)
                    if len(checker_splitted) != 1:
                        checker_name_splitted = checker_splitted[0]
                        checker_rules = checker_splitted[1]
                    else:
                        checker_name_splitted = "eslint"
                        checker_rules = checker_splitted[0]

                    if type(list(rules.values())[i]) == str:
                        severity = get_severity(list(rules.values())[i])
                    elif type(list(rules.values())[i]) == list:
                        severity = get_severity(list(rules.values())[i][0])
                    else:
                        raise "Unexpected config"

                    if severity is not None:
                        url = DOC_ESLINT_PLUGINS[checker_name_splitted]["doc_url"]
                        format = DOC_ESLINT_PLUGINS[checker_name_splitted]["format"]
                        if checker_name == "tsdoc/syntax":
                            labels[checker_name] = [
                                f"doc_url:{url}",
                                f"severity:{severity}"
                            ]
                        else:
                            labels[checker_name] = [
                                f"doc_url:{os.path.join(url, checker_rules) + format}",
                                f"severity:{severity}"
                            ]

            if "extends" in ov:
                extend = ov["extends"]
                for ex in extend:
                    ex_plugin = ex.split(":")[1]
                    if ex_plugin in RULES_EXTENDS_ESLINT_PLUGINS:
                        for k in RULES_EXTENDS_ESLINT_PLUGINS[ex_plugin]:
                            labels[k] = RULES_EXTENDS_ESLINT_PLUGINS[ex_plugin][k]

        f.close()

    config_data = {
        "analyzer": "pylint",
        "labels": labels
    }

    with open(file_to_write, "w") as outfile:
        str_ = json.dumps(config_data, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
        outfile.write(str_)


if __name__ == "__main__":
    main()
