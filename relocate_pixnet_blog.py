""" Convert All Files in PIXNET Album into .JPG Format
# Description:
    Build the .md files from my PIXNET exported blog backup file.
# Author: Shin-Fu (Kelvin) Wu
# Date: 2017/07/14
"""
import os

def generate_post(init_ind, end_ind, file_list):
    file_content = file_list[init_ind:end_ind - 1]
    title = file_list[init_ind].decode("utf-8")[7:-2]

    # Get rid of special characters from filename
    if ']' in title:
        title = title[title.index(']')+1:]
    title = title.replace(' - ', '-')
    title = title.replace(' ', '-')
    title = title.replace('.', '')
    title = title.replace('，', '-')
    title = title.replace('？', '')
    title = title.replace('！', '')
    title = title.replace('☆', '-')
    title = title.replace('(', '')
    title = title.replace(')', '')
    title = title.replace('、', '-')
    title = title.replace('~', '-')

    date = file_list[init_ind+2].decode("utf-8")[6:16]
    file_name = '%s-%s-%s-%s.md' %(date[-4:], date[:2], date[-7:-5], title)
    return file_content, file_name

def generate_metadata(metadata):
    output_metadata = []
    output_metadata.append(b'---\n')
    output_metadata.append(b'layout: single\n')

    for line in metadata:
        if 'TITLE'.encode('utf-8') in line:

            title = str(line, 'utf-8')
            if ']' in title:
                title = title[title.index(']')+1:]
#            title = title.replace(' - ', '-')
#            title = title.replace(' ', '-')
#            title = title.replace('.', '')
#            title = title.replace('，', '-')
#            title = title.replace('？', '')
#            title = title.replace('！', '')
#            title = title.replace('☆', '-')
#            title = title.replace('(', '')
#            title = title.replace(')', '')
#            title = title.replace('、', '-')
#            title = title.replace('~', '-')

            output_metadata.append(b'title: %s' %title.encode('utf-8'))
        if 'DATE'.encode('utf-8') in line:
            if 'AM'.encode('utf-8') in line:
                output_metadata.append(b'date: %s-%s-%s %s:%s:%s\n' %(line[12:16], line[6:8], line[9:11], line[17:19], line[20:22], line[23:25]))
            else:
                hour = int(line[17:19])
                if hour < 12:
                    time = str(hour+12).encode('utf-8')
                else:
                    time = str(hour).encode('utf-8')
                output_metadata.append(b'date: %s-%s-%s %s:%s:%s\n' %(line[12:16], line[6:8], line[9:11], time, line[20:22], line[23:25]))
        if 'PRIMARY CATEGORY'.encode('utf-8') in line:
            output_metadata.append(b'categories:\n')
            output_metadata.append(b'- %s\n' %line[18:-2])
        if 'TAGS'.encode('utf-8') in line:
            tag_list=str(line[6:-2], 'utf-8').split(',')
            output_metadata.append(b'tags:\n')
            for tag in tag_list:
                output_metadata.append(b'- %s\n' %(tag[1:-1].encode('utf-8')))
    output_metadata.append(b'---\n')
    output_metadata.append(b'\n')
    return output_metadata

def generate_content(content):
    output_content = []
    for line in content:
        if '&nbsp;'.encode('utf-8') in line:
            pass
        elif '<p>'.encode('utf-8') in line:
            output_content.append(b'%s\n' %line[3:-6])
        elif 'COMMENT'.encode('utf-8') in line:
            output_content = output_content[:-1]
            break
        else:
            output_content.append(line)
    return output_content

if __name__ == '__main__':

    """Section 1: Setting File and Path"""
    ###########################################################################

    file_path = os.path.join(os.path.dirname(__file__), 'pixnet_backup', 'blog-export-mt-KWbuster-20170714081020.txt')
    post_dir = os.path.join(os.path.dirname(__file__), 'posts')

    if not os.path.exists(post_dir):
        os.makedirs(post_dir)

    """Section 2: Divide the Posts from single .TXT File"""
    ###########################################################################
    with open(file_path, 'rb') as read_file:
        file_list = read_file.readlines()

    init_ind, end_ind = 0, 0
    while init_ind < len(file_list) and end_ind < len(file_list):
        # Divide posts by "TITLE"
        if (end_ind != 0) and ('TITLE'.encode('utf-8') in file_list[end_ind]):
            file_content, file_name = generate_post(init_ind, end_ind, file_list)

            # Write the post
            if 'publish'.encode('utf-8') in file_content[5]:
                print('process... %s' %file_name)
                with open(post_dir + '/' + file_name, 'wb') as write_file:
                    write_file.writelines(file_content)
            init_ind = end_ind
        end_ind += 1

    # last post
    file_content, file_name = generate_post(init_ind, end_ind, file_list)

    if 'publish'.encode('utf-8') in file_content[5]:
        print('process... %s' %file_name)
        with open(post_dir + '/' + file_name, 'wb') as write_file:
            write_file.writelines(file_content)

    """Section 3: Organize Markdown Files"""
    ###########################################################################

    post_files = [x[2] for x in os.walk(post_dir)][0]
    for post_file in post_files:
        with open(post_dir + '/' +post_file, 'rb') as read_file:
            post_content = read_file.readlines()

        print('Markdown...%s' %post_file)
        # Divide the post into metadata and content parts
        for ind in range(len(post_content)):
            if 'BODY'.encode('utf-8') in post_content[ind]:
                metadata = post_content[:ind]
                content = post_content[ind+1:-1]

        # Jekyll Markdown
        output_metadata = generate_metadata(metadata)
        output_content = generate_content(content)

        with open(post_dir + '/' +post_file, 'wb') as write_file:
            write_file.writelines(output_metadata+output_content)
