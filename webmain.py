import web
import os

urls = ('/upload', 'Upload')

class Upload:

    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return open(r'upload.html', 'r').read()

    def POST(self):

        try:
            x = web.input(myfile={})

            filedir = 'submit' # change this to the directory you want to store the file in.
            if 'myfile' in x: # to check if the file-object is created
                filepath = x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
                filename = filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
                fout = open(filedir +'/'+ filename,'w+') # creates the file where the uploaded file should be stored
                fout.write(x.myfile.file.read().decode('utf-8')) # writes the uploaded file to the newly created file.
                fout.close() # closes the file, upload complete.

                if filename[-2:] == '.c':
                    # start analyze
                    os.system('echo check')
                    os.system('python3 grade.py > result.txt')
                    os.system('rm ' + filedir + '/' + filename)
                    print('[file deleted]')

                    resultWeb = open(r'result.html', 'r').read()

                    result = open('result.txt', 'r').read()
                    if(result.find('Failed.') != -1):
                        resultWeb = resultWeb[: resultWeb.find('<!--result-->')] + '\n<h3><strong style="color: red"> Test Failed</strong></h3><br>\n' + result + '\n' + resultWeb[resultWeb.find('<!--result-->') + len('<!--result-->'):]
                    else:
                        # add result to website
                        resultWeb = resultWeb[: resultWeb.find('<!--result-->')] + '\n<h3><strong style="color: green"> Test Passed</strong></h3><br>\n' + result + '\n' + resultWeb[resultWeb.find('<!--result-->') + len('<!--result-->'):]

                else:
                    resultWeb = open(r'error.html', 'r').read()
                    resultWeb = resultWeb[:resultWeb.find('<!--file-->')] + filename +resultWeb[resultWeb.find('<!--file-->'):]
                    os.system('rm ' + filedir + '/' + filename)
                    print('[file deleted]')

                return resultWeb
        except:
            resultWeb = open(r'error.html', 'r').read()
            resultWeb = resultWeb[:resultWeb.find('<!--file-->')] + 'ERROR:\n No file uploaded or internal error occured while uploading the file.' + resultWeb[resultWeb.find('<!--file-->'):]

            return resultWeb

        raise web.seeother('/upload')

if __name__ == "__main__":
   app = web.application(urls, globals())
   app.run()