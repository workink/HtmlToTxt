from absl import flags
from absl import app
from bs4 import BeautifulSoup
from bs4.element import Comment
import csv
import os
import tensorflow as tf
import urllib2
import uuid

FLAGS = flags.FLAGS
flags.DEFINE_string('input_csv', None, 'The input csv file containing webpage urls')
flags.DEFINE_string('output_dir', None, 'The directory for output')
flags.mark_flag_as_required('input_csv')
flags.mark_flag_as_required('output_dir')

HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}


def tag_visible(element):
    """Function to decide tag visibility.

    Args:
        element: texts in the parsed html.

    Returns:
        Ture if wanting to save in the final results; False if not.

    """
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    elif isinstance(element, Comment):
        return False
    return True


def get_content(html):
    """Function to get processed main texts from html.

    Args:
        html: html for processing.

    Returns:
        A text string in the web page.
    """
    soup = BeautifulSoup(html, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    content = " ".join(t.strip() for t in visible_texts).encode('utf-8').strip()
    return content


def get_title(html):
    """Function to get the title in the html"""
    soup = BeautifulSoup(html, 'html.parser')
    return soup.title.string.encode('utf-8').strip()


def write_to_file(title, content, file_path):
    """Function to write the title and content to the given file"""
    if tf.io.gfile.exists(file_path):
        tf.io.gfile.remove(file_path)
    with tf.io.gfile.GFile(file_path, 'a+') as f:
        f.write('[TITLE]:\n')
        f.write(title)
        f.write('\n' * 3)
        f.write('[CONTENT]:\n')
        f.write(content)
    return


def main(unused_argv):
    input_csv = FLAGS.input_csv
    output_dir = FLAGS.output_dir

    if not tf.io.gfile.exists(output_dir):
        tf.io.gfile.makedirs(output_dir)

    mapping_csv_filename = 'mapping_csv_' + str(uuid.uuid4()) + '.csv'
    mapping_csv = tf.io.gfile.GFile(os.path.join(output_dir, mapping_csv_filename), 'a')
    mapping_csv_fieldnames = ['URL', 'MappingFilename']
    print('The mapping csv file is %s' % mapping_csv_filename)
    mapping_csv_writer = csv.DictWriter(mapping_csv, fieldnames=mapping_csv_fieldnames)
    mapping_csv_writer.writeheader()

    with tf.io.gfile.GFile(input_csv, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            url = row['URL']
            req = urllib2.Request(url, None, HEADER)
            try:
                html = urllib2.urlopen(req).read()
            except urllib2.HTTPError as e:
                print(e.code)
                print(url)
                return ''
            content = get_content(html)
            title = get_title(html)
            # Save to files.
            output_filename = 'output_file_' + str(uuid.uuid4()) + '.txt'
            file_path = os.path.join(output_dir, output_filename)
            write_to_file(title, content, file_path)
            mapping_csv_writer.writerow({'URL': url, 'MappingFilename': output_filename})

    mapping_csv.close()


if __name__ == '__main__':
    app.run(main)
