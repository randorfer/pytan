
"""
Ask a manual question using human strings by referencing the name of a single sensor that takes parameters, but supplying only two of the four parameters that are used by the sensor.

Also supply a sensor filter that limits the column data that is shown to values that match the regex '.*Shared.*', and a sensor filter option that re-fetches any cached data that is older than 3600 seconds.

No question filters or question options supplied.
"""
# Path to lib directory which contains pytan package
PYTAN_LIB_PATH = '../lib'

# connection info for Tanium Server
USERNAME = "Tanium User"
PASSWORD = "T@n!um"
HOST = "172.16.31.128"
PORT = "444"

# Logging conrols
LOGLEVEL = 2
DEBUGFORMAT = False

import sys, tempfile
sys.path.append(PYTAN_LIB_PATH)

import pytan
handler = pytan.Handler(
    username=USERNAME,
    password=PASSWORD,
    host=HOST,
    port=PORT,
    loglevel=LOGLEVEL,
    debugformat=DEBUGFORMAT,
)

print handler

# setup the arguments for the handler method
kwargs = {}
kwargs["sensors"] = u'Folder Name Search with RegEx Match{dirname=Program Files,regex=Microsoft.*}, that regex match:.*Shared.*, opt:max_data_age:3600'
kwargs["qtype"] = u'manual_human'

# call the handler with the ask method, passing in kwargs for arguments
response = handler.ask(**kwargs)
import pprint, io

print ""
print "Type of response: ", type(response)

print ""
print "Pretty print of response:"
print pprint.pformat(response)

print ""
print "Equivalent Question if it were to be asked in the Tanium Console: "
print response['question_object'].query_text

# create an IO stream to store CSV results to
out = io.BytesIO()

# call the write_csv() method to convert response to CSV and store it in out
response['question_results'].write_csv(out, response['question_results'])

print ""
print "CSV Results of response: "
out = out.getvalue()
if len(out.splitlines()) > 15:
    out = out.splitlines()[0:15]
    out.append('..trimmed for brevity..')
    out = '\n'.join(out)
print out


'''Output from running this:
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
2014-12-08 16:24:50,266 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" from all machines)
2014-12-08 16:24:55,284 INFO     question_progress: Results 0% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" from all machines)
2014-12-08 16:25:00,307 INFO     question_progress: Results 17% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" from all machines)
2014-12-08 16:25:05,326 INFO     question_progress: Results 67% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" from all machines)
2014-12-08 16:25:10,344 INFO     question_progress: Results 83% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" from all machines)
2014-12-08 16:25:15,369 INFO     question_progress: Results 100% (Get Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" from all machines)

Type of response:  <type 'dict'>

Pretty print of response:
{'question_object': <taniumpy.object_types.question.Question object at 0x102967b90>,
 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x102b2fd50>}

Equivalent Question if it were to be asked in the Tanium Console: 
Get Folder Name Search with RegEx Match[No, Program Files, No, ] contains "Shared" from all machines

CSV Results of response: 
Count,"Folder Name Search with RegEx Match[No, Program Files, No, ]"
4,[no results]
1,C:\Program Files\Common Files\Microsoft Shared\VS7Debug
2,C:\Program Files\Common Files\Microsoft Shared\ink\ar-SA
2,C:\Program Files\Common Files\Microsoft Shared\ink\ru-RU
2,C:\Program Files\Common Files\Microsoft Shared\ink\fsdefinitions\keypad
2,C:\Program Files\Common Files\Microsoft Shared\ink
2,C:\Program Files\Common Files\Microsoft Shared\ink\sv-SE
2,C:\Program Files\Common Files\Microsoft Shared\ink\uk-UA
2,C:\Program Files\Common Files\Microsoft Shared\ink\sl-SI
2,C:\Program Files\Common Files\Microsoft Shared\ink\hu-HU
2,C:\Program Files\Common Files\Microsoft Shared\ink\zh-TW
2,C:\Program Files\Common Files\Microsoft Shared\ink\zh-CN
2,C:\Program Files\Common Files\Microsoft Shared\ink\fi-FI
2,C:\Program Files\Common Files\Microsoft Shared
..trimmed for brevity..

'''
