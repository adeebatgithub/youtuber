import os
import sys

from youtuber import Youtuber

def banner():
    print("="*56)
    print("\t\t\tYOUTUBER")
    print("="*56)

def get_or_set_path():
    if not os.path.exists("dpath.py"):
        path = input("[+] path to download: ")
        content = f'download_path = "{path}"'
        with open("dpath.py", "w") as file:
            file.write(content)
    import dpath
    return dpath.download_path

def get_res_or_error(tags, res):
    try:
        return tags[res]
    except KeyError:
        print("[!] resolution not found")

def get_max_aud_res(keys):
    max_len = max([len(key) for key in keys])
    sorted_keys = [key for key in keys if len(key) == max_len]
    suffix_removed_keys = [key.replace("kbps", "") for key in sorted_keys]
    max_res = max(suffix_removed_keys)
    return f"{max_res}kbps"


if __name__ == "__main__":

    argv = sys.argv

    banner()
    quit()
    path = get_or_set_path()

    youtuber = Youtuber()
    youtuber.path = path

    if "-url" in argv:
        url = argv[argv.index("-url") + 1]
    else:
        url = input("[+] url: ")
        print("[!] checking url...")
    if not youtuber.check_url(url):
        print("[!] the provided url is not valid")
        quit()

    if "-aud" in argv:
        youtuber.aud = True

    print("[!] getting video...")
    youtuber.get_video(url)
    tags = youtuber.get_res()
   
    if "-res" in argv:
        res = argv[argv.index("-res")]
    else:
        if "-aud" not in argv:
            print("[~] Resolutions: ", *sorted(tags.keys()))
            res = input("[+] Resolution: ")
    if "-aud" in argv:
        res = get_max_aud_res(tags.keys())
        
    tag = get_res_or_error(tags, res)

    print("[~] downloading")
    print(f"[~] title: {youtuber.get_title()}")
    youtuber.download(tag)
    print("[!] downloaded")

