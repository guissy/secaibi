import os
import subprocess
import json
import sys
from mimetypes import MimeTypes
import urllib

cur_file = sys.argv[1] if len(sys.argv) > 1 else '~/Downloads/ju.png'
mime = MimeTypes()
url = urllib.pathname2url(cur_file)
mime_type = mime.guess_type(url)[0]
imgtype = mime_type.split('/')[1]
#raise Exception(cur_file)
print(cur_file)
upfile = subprocess.Popen(
    "curl 'https://www.secaibi.com/designtools/api/image.html?tag=formatconvert&restful_override_method=PUT&qqfile=ju"
    ".png' -X POST -H 'Cookie: Hm_lvt_a3ba71e939d2d772cf99c08dea697a3f=1555003930; "
    "Hm_lpvt_a3ba71e939d2d772cf99c08dea697a3f=1555004351' -H 'Origin: https://www.secaibi.com' -H 'Accept-Encoding: "
    "gzip, deflate, br' -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8' -H 'X-File-Name: ju.png' -H 'User-Agent: "
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3753.4 "
    "Safari/537.36' -H 'Content-Type: application/octet-stream' -H 'Accept: */*' -H 'X-Mime-Type: {}' -H "
    "'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' -H 'Referer: "
    "https://www.secaibi.com/designtools/media/pages/formatconvert.html' --data-binary '@{}'  --compressed".format(
        mime_type, cur_file), shell=True, stdout=subprocess.PIPE).stdout.read()

upfile_dict = json.loads(upfile)
if 'id' in upfile_dict and upfile_dict['id']:
    id = upfile_dict['id']
    dofile = subprocess.Popen(
        "curl 'https://www.secaibi.com/designtools/api/resizer-action' -H 'Cookie: "
        "Hm_lvt_a3ba71e939d2d772cf99c08dea697a3f=1555003930; Hm_lpvt_a3ba71e939d2d772cf99c08dea697a3f=1555004351' -H "
        "'Origin: https://www.secaibi.com' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: zh-CN,"
        "zh;q=0.9,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 ("
        "KHTML, like Gecko) Chrome/75.0.3753.4 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; "
        "charset=UTF-8' -H 'Accept: */*' -H 'Referer: "
        "https://www.secaibi.com/designtools/media/pages/formatconvert.html' -H 'X-Requested-With: XMLHttpRequest' -H "
        "'Connection: keep-alive' --data 'action=compress&srcid={}"
        "&srcname=ju.png&param_limit_width=origin&param_accept_lossy=true&param_jpeg_quality=0' "
        "--compressed".format(id, imgtype), shell=True, stdout=subprocess.PIPE).stdout.read()
    print(id, imgtype, dofile)
    dofile_dict = json.loads(dofile)

    if 'success' in dofile_dict and dofile_dict['success']:
        dstid = dofile_dict['dstid']
        # file_name = '.'.join(os.path.basename(cur_file).split('.')[:-1])
        cmd = "curl 'https://www.secaibi.com/designtools/api/image/{}.bin?filename=ju.jpeg' -o {}"
        file = subprocess.Popen(cmd.format(dstid, cur_file), shell=True, stdout=subprocess.PIPE).stdout.read()
        subprocess.Popen('echo ok', shell=True, stdout=subprocess.PIPE).stdout.read()
sys.exit()
