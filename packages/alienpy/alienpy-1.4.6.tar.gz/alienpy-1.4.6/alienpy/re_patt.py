import re

REGEX_PATTERN_TYPE = type(re.compile('.'))
guid_regex = re.compile('[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}', re.IGNORECASE)  # regex for identification of GUIDs
cmds_split = re.compile(';|\n')  # regex for spliting chained commands
specs_split = re.compile('@|,')  # regex for spliting the specification of cp command

ignore_comments_re = re.compile('^\\s*(#|;|//)+', re.MULTILINE)  # identifiy a range of comments
emptyline_re = re.compile('^\\s*$', re.MULTILINE)  # whitespace line

lfn_prefix_re = re.compile('(alien|file){1}(:|/{2})+')  # regex for identification of lfn prefix


if __name__ == '__main__':
    print('This file should not be executed!', file = sys.stderr, flush = True)
    sys.exit(95)

