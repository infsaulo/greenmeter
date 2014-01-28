
def extract_tags(line):
    tags = []
    if ":" in line:
        for token in line.split():
            if ":" in token:
                token = token.split(":")[0]
                tags.append(int(token))
    else:
        for token in line.split():
            tags.append(int(token))
    return tags


