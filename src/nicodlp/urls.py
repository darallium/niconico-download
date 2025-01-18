import requests
from bs4 import BeautifulSoup
import argparse


def get_nc_link_hrefs(url):
    """
    指定されたURLのページから、NC-Linkクラスを持つすべてのaタグのhrefを取得します。

    Args:
        url: ターゲットURLの文字列。

    Returns:
        NC-Linkクラスを持つaタグのhrefのリスト。
        リクエストに失敗した場合はNoneを返します。
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTPエラーをチェック

        soup = BeautifulSoup(response.content, "html.parser")
        nc_links = soup.find_all("a", class_="NC-Link")

        hrefs = [link["href"] for link in nc_links if "href" in link.attrs]
        return hrefs

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def save_hrefs_to_file(hrefs, filename="list.txt"):
    try:
        existing_hrefs = set()
        try:
            with open(filename, "r") as f:
                for line in f:
                    existing_hrefs.add(line.strip())
        except FileNotFoundError:
            pass

        with open(filename, "a") as f:
            for href in hrefs:
                if href not in existing_hrefs:
                    f.write(href + "\n")
                    existing_hrefs.add(href)
    except Exception as e:
        print(f"Error saving hrefs to file: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="指定されたURLのページから、指定されたクラスを持つすべてのaタグのhrefを取得します。"
    )
    parser.add_argument("url", help="ターゲットURL")
    parser.add_argument(
        "-f",
        "--filename",
        default="list.txt",
        help="保存先のファイル名 (デフォルト: list.txt)",
    )
    args = parser.parse_args()
    if args.url:
        href_list = get_nc_link_hrefs(args.url)
    else:
        print("aborted")
        exit(1)

    if href_list:
        print("NC-Link hrefs:")
        for href in href_list:
            print(href)
        save_hrefs_to_file(href_list, args.filename)


# 使用例
if __name__ == "__main__":
    main()
