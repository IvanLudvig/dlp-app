from django.shortcuts import render
from django.http import HttpResponse
import paramiko
from django.core.files.storage import default_storage
import stat
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.template import loader
from pathlib import Path
import os

host = '164.92.134.201'

from django.template import RequestContext, Template

    
@login_required
def list_dir(request):
    dir = request.GET.get('dir', '.')
    dir = os.path.normpath(dir)
    print(dir)

    username = str(request.user)
    pkey_path = 'keys/' + username + '.private'
    pkey = paramiko.RSAKey(filename=pkey_path)
    connection = paramiko.Transport(host, 22)

    try:
        connection.connect(None, username=username, pkey=pkey)
    except paramiko.AuthenticationException as error:
        return render(request, 'registration/game404.html')

    # ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)
    sftp = paramiko.SFTPClient.from_transport(connection)

    files_attr = sftp.listdir_attr(path=dir)
    file_paths = []
    file_names = []
    dir_paths = [dir+'/../']
    dir_names = []
    if dir != '.':
        dir_names.append('..')
    for fileattr in files_attr:
        if stat.S_ISDIR(fileattr.st_mode):
            full_path = (dir+'/'+fileattr.filename)
            dir_paths.append(full_path)
            dir_names.append(fileattr.filename)
        else:
            full_path = (dir+'/'+fileattr.filename)
            file_paths.append(full_path)
            file_names.append(fileattr.filename)
    # return HttpResponse(response)
    return render(request, 'listdir/listdir.html', {
        'files': zip(file_paths, file_names), 
        'dirs': zip(dir_paths, dir_names),
        'username': request.user,
        'dir': dir
    })


@login_required
def read_file(request):
    file_name = request.GET['filename']
    print(file_name)

    username = str(request.user)
    pkey_path = 'keys/' + username + '.private'

    ssh = paramiko.SSHClient()
    pkey = paramiko.RSAKey(filename=pkey_path)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, key_filename=pkey_path)

    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(f'python3 /usr/bin/dlp.py {file_name}')
    print(ssh_stdout)
    response = HttpResponse(ssh_stdout, content_type="application/force-download")
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name.split('/')[-1])
    return response



from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
import os

def handle_uploaded_file(request, _f):
    user = str(request.user)
    with open('keys/' + user + '.private', 'w') as f:
        f.write(_f.file.read().decode('ascii'))


# Imaginary function to handle an uploaded file.
@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        handle_uploaded_file(request, request.FILES['file'])
        return HttpResponseRedirect('/dlp/list_dir?dir=/')
    else:
        form = UploadFileForm()
    return render(request, 'registration/upload.html', {'form': form})


