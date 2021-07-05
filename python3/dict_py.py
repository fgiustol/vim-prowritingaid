# dict_py.py
from __future__ import print_function
import ProWritingAidSDK
from ProWritingAidSDK.rest import ApiException
import vim

#this function returns the windows of a given buffer
def getwin(b):
    for w in vim.windows:
        if w.buffer.name == b.name:
            return w
    return None


#main function
def eval_txt(fullb, end_line, scratchb):

    if fullb.mark('<') is None:
        # get up to the cursor
        offset=0
        b = fullb[0:end_line]
    else:
        # get visual selection
        offset = fullb.mark('<')[0]-1
        b = fullb[offset:fullb.mark('>')[0]]

    # add spaces to a tmp buffer, so it will match with the string sent later to PWA 
    b_spaces = []
    for bu_line in b:
        b_spaces.append(bu_line.ljust(len(bu_line)+1))

    # save line and char indexes of the tmp buffer with spaces into a list of tuples 
    textmap=[]
    for i,string in enumerate(b_spaces):
        for j,char in enumerate(string):
            textmap.append((i,j))

    wrong_sent = ' '.join(b[:]) 
    
    configuration = ProWritingAidSDK.Configuration()
    configuration.host = 'https://api.prowritingaid.com'
    configuration.api_key['licenseCode'] = 'codegoeshere'

    # create an instance of the API class
    api_instance = ProWritingAidSDK.TextApi(ProWritingAidSDK.ApiClient('https://api.prowritingaid.com'))
    try:
        api_request = ProWritingAidSDK.TextAnalysisRequest(wrong_sent,
                                                           ["grammar"],
                                                           "General",
                                                           "en_UK")
        api_response = api_instance.post(api_request)
    
    except ApiException as e:
        print("Exception when calling API: %s\n" % e)
    tags = api_response.result.tags
    
    vim.current.window=getwin(fullb)
    
    for tag in tags:
        line = textmap[tag.start_pos][0]
        col_start = textmap[tag.start_pos][1]
        col_end = textmap[tag.end_pos][1]
        if col_start<=col_end: # avoid to signal a space after a '.' 
            vim.eval(f'matchaddpos("Error", [[{line+offset+1},{col_start+1},{col_end-col_start+1}]])')
            scratchb.append("Error in line "+str(line+offset+1)+ " col "+str(col_start+1))
            sugg=', '.join(map(str,tag.suggestions))
            scratchb.append("Suggestions: "+sugg)
            scratchb.append(" ")






