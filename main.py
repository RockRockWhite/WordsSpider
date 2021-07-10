import request
import bs4


def get_trans_and_example(word):

    url = f"https://dict.youdao.com/search?q={word}&keyfrom=new-fanyi.smartResult"
    headers = {
        "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        r"Chrome/88.0.4324.150 Safari/537.36"
    }

    # 发送请求
    res = request.get(url=url, headers=headers)

    # 处理请求
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    word_trans = soup.find("div", class_="trans-container").text
    word_trans = word_trans.split("\n\n[")[0]

    word_trans = word_trans.split("\n\n")[1]

    examples = soup.find_all("div", class_="examples")

    best_example = ""

    for each in examples:

        if best_example == "":
            best_example = each.text

        else:
            best_example = (
                each.text if len(best_example) > len(each.text) else best_example
            )

    return word + "\n\n" + word_trans + "\n" + best_example


def get_words_list(path):

    file = open(path, "rt", encoding="utf-8")
    file_context = file.read()
    file.close()

    return file_context


def write_result(path, result):

    file_to_write = open(path, "w", encoding="utf-8")
    file_to_write.write(result)
    file_to_write.close()


def main():
    # 读入文件
    print("reading words.txt...")
    words_text = get_words_list("words.txt")
    words_list = words_text.split("\n")

    result = ""

    for each in words_list:
        print(f"getting {each}...")
        curr_result = get_trans_and_example(each)
        result += "\n\n"
        result += curr_result

    write_result("result.txt", result)

    print("Succeed in writing to  result.txt...")


if __name__ == "__main__":
    main()