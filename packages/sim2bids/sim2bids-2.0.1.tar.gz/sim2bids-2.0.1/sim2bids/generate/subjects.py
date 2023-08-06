import os
import csv
import re
from pathlib import Path

import numpy as np
import pandas as pd

# import sim2bids

from sim2bids.app import app
from collections import OrderedDict
import sim2bids.preprocess.preprocess as prep
from sim2bids.convert import convert
from sim2bids.app import utils

GLOBAL_FILES = []


# collect rhythms, speeds, and global coupling
# RHYTHMS_PARAMS = dict(alpha=[], beta=[], gamma=[], delta=[], theta=[])


class Files:
    def __init__(self, path, files):
        self.path = path
        self.files = files
        self.subs = OrderedDict()

        # get all files' absolute paths
        self.content = utils.get_content(path, files)

        # get all files
        app.ALL_FILES = self.content

        # get all files' unique names
        self.basename = set(utils.get_content(path, files, basename=True))

        # check for multi-subject in one folder
        self.match = find_matches(self.content)

        # check if the input is for single-subject or multi-subject
        app.MULTI_INPUT = self.check_input()

        # define a variable that is going to check whether input
        # contains sessions-based subject. Sessions include `ses-preop` and 'ses-postop'
        self.ses_found = False

        # traverse folders
        prep.reset_index()
        self.traverse_files()

    def check_input(self):
        # weights are the essential files for each subject,
        # therefore, finding the number of weights will reveal
        # whether the file folder is multi-folder or not
        basename = [os.path.basename(x) for x in self.content]
        weights = 0

        for name in basename:
            if 'weight' in name:
                weights += 1
        return False if weights == 1 else True

    def traverse_files(self):
        # if the whole folder is passed, open that folder
        path, files, changed = self.path, self.files, False

        if len(files) == 1 and os.path.isdir(os.path.join(path, files[0])) and files[0] not in ['ses-preop',
                                                                                                'ses-postop']:
            path = os.path.join(path, files[0])
            files = os.listdir(path)

        # ====================================================
        #          TRAVERSE MULTI-SUBJECT INSTANCES
        # ====================================================

        if app.MULTI_INPUT:

            # traverse multi-subject in one folder structure
            if len(self.match) > 0:

                for k, v in get_unique_subs(self.match, self.content).items():
                    # create a new ID
                    sid = self.create_sid_sub()
                    self.subs[sid].update(prepare_subs([os.path.join(path, x) for x in v], sid))
            else:
                for file in files:
                    sid = self.get_sid(path, file)

                    # Step 5: get all content
                    if os.path.isdir(os.path.join(path, file)):
                        all_files = os.listdir(os.path.join(path, file))
                    else:
                        all_files = os.listdir(path)

                    # Step 6: traverse ses-preop if present
                    if 'ses-preop' in all_files:
                        app.SESSIONS = True
                        self.save_sessions('ses-preop', all_files, sid, os.path.join(path, file))

                    # Step 7: traverse ses-postop if present
                    if 'ses-postop' in all_files:
                        app.SESSIONS = True
                        self.save_sessions('ses-postop', all_files, sid, os.path.join(path, file))

                    if 'ses-preop' not in all_files and 'ses-postop' not in all_files:
                        if os.path.basename(path) == file:
                            self.subs[sid] = prepare_subs(utils.get_content(path.replace(file, ''), file), sid)
                        else:
                            self.subs[sid] = prepare_subs(utils.get_content(path, file), sid)
        else:
            # check if there are no folders inside
            sid = self.create_sid_sub()
            self.save_sessions('ses-preop', files, sid, os.path.join(path, 'ses-preop'))
            self.save_sessions('ses-postop', files, sid, os.path.join(path, 'ses-postop'))

            if not self.ses_found:
                self.create_sid_sub()
                self.subs[sid] = prepare_subs(utils.get_content(path, files), sid)

        # ==========================================
        #               SAVE CLEAN SUBJECTS
        # ==========================================

        # create an empty dictionary to store clean subjects
        subs = OrderedDict()

        # iterate over created subjects and save only non-None instances
        for k, v in self.subs.items():
            if k:
                subs[k] = v

        self.subs = subs

    def get_sid(self, path, file):
        if os.path.isdir(os.path.join(path, file)):
            if 'sub-' in file:
                return file
            else:
                return self.create_sid_sub()

    def save_sessions(self, ses, files, sid, path):
        if ses in files:
            self.ses_found = True
            app.SESSIONS = True
            if sid not in self.subs.keys():
                self.subs[sid] = OrderedDict()
            if ses not in self.subs[sid].keys():
                self.subs[sid][ses] = OrderedDict()

            self.subs[sid][ses].update(prepare_subs(utils.get_content(path, ses), sid))

    def create_sid_sub(self):
        self.check_empty()

        sid = prep.create_uuid()
        self.subs[sid] = {}

        return sid

    def check_empty(self):
        temp, to_delete = OrderedDict(), []

        for k, v in self.subs.items():
            if len(v) > 0:
                temp[k] = v

        # iterate over existing ids and correct indexing if necessary
        for i, (k, v) in enumerate(temp.items(), start=1):
            if not k.endswith(str(i)):
                idx = f'sub-0{i}' if i < 10 else f'sub-{i}'
                to_delete.append(k)
                temp[idx] = v

        for idx in to_delete:
            del temp[idx]

        self.subs = temp


def traverse_single(path, selected, sid, ses=None):
    if ses is not None:
        return prepare_subs(utils.get_content(path, ses), sid)
    else:
        return prepare_subs(utils.get_content(path, selected), sid)


def find_matches(paths):
    unique_ids = []

    for path in paths:
        match = re.findall('[A-Z]{2,3}_[0-9]{4,}', path)
        if len(match) > 0 and not path.endswith('.h5'):
            unique_ids.append(match[0])

    return list(set(unique_ids))


def get_unique_subs(match, contents):
    subs = OrderedDict()

    for idx in range(len(match)):
        subs[match[idx]] = [x for x in contents if match[idx] in x]

    return subs


def prepare_subs(file_paths, sid):
    subs = {}

    for file_path in file_paths:
        if 'CHANGES' in file_path or 'participants' in file_path or 'README' in file_path:
            app.MISSING.append(file_path)
            continue

        file_path = check_name(file_path)

        name = get_filename(file_path)

        if file_path.endswith('.h5'):
            name = name.split('_')[0] + '.h5'
        else:
            name = name.split('.')[0]

        desc = app.DESC

        # get extensions
        ext = os.path.basename(file_path).split('.')[-1]

        # check if file is a numpy array
        if ext.endswith('npy'):
            new_path = os.path.basename(file_path.replace(ext, 'txt'))
            file = np.load(file_path)
            np.savetxt(os.path.join(os.path.dirname(file_path), new_path), file)
            os.remove(file_path)

            file_path = check_name(os.path.join(os.path.dirname(file_path), new_path))

        # check if file ends with CSV or dat, if true, change file
        # extension to plain TXT. It's necessary so that there's minimal
        # number of "if" statements in the future traversals
        if ext.endswith('csv') or ext.endswith('dat'):
            # instantiate a new path
            new_path = file_path.replace(ext, 'txt')

            if os.path.exists(file_path):
                p = Path(file_path)
                p.rename(p.with_suffix('.txt'))

                # set the new path
                file_path = new_path

        if not file_path.endswith('txt'):
            continue
        else:
            sep = find_separator(file_path)

            if sep == 'remove':
                os.remove(file_path)
                continue

            if 'weights' in file_path:
                if 'scthran' in file_path.lower():
                    name = f'desc-SCthrAn_weights'
                elif 'scnotthran' in file_path.lower():
                    name = f'desc-SCnotthrAn_weights'
            else:
                name = get_name(file_path)

            subs[name] = {
                'name': name,
                'fname': os.path.basename(file_path),
                'sid': sid,
                'desc': desc,
                'sep': sep,
                'path': file_path,
                'ext': get_file_ext(file_path),
            }

            if subs[name]['name'] in ['centres', 'centre']:
                app.CENTERS = True

            # save network path
            if len(convert.NETWORK) < 2:
                desc, fname = app.DESC, name.split('.')[0]

                if fname in ['weights', 'distances']:
                    if 'ses-preop' in subs[name]['path'] in subs[name]['path']:
                        convert.NETWORK.append(f'../{sid}/ses-preop/net/{sid}_desc-{app.DESC}_{fname}.json')
                    elif 'ses-postop' in subs[name]['path'] in subs[name]['path']:
                        convert.NETWORK.append(f'../{sid}/ses-postop/net/{sid}_desc-{app.DESC}_{fname}.json')
                    else:
                        convert.NETWORK.append(f'../{sid}/net/{sid}_desc-{app.DESC}_{fname}.json')

                    convert.NETWORK = list(set(convert.NETWORK))

    return subs


def check_name(path):
    basename = os.path.basename(path)
    new_path = path

    if 'tract_lengths' in basename:
        dist = os.path.join(path.replace(basename, ''), 'distances.txt')
        if os.path.exists(dist):
            os.remove(dist)

        new_path = path.replace(basename, 'distances.txt')
    elif 'orientation' in basename:
        new_path = path.replace(basename, 'normals.txt')

    if path != new_path:
        os.rename(path, new_path)

    return new_path


def get_name(path, return_rhythm=False):
    # get file's basename (=without root directory)
    base = os.path.basename(path)

    # instantiate speed, global coupling, and rhythms
    speed, g, series = None, None, None

    # iterate over rhythms if exist to get naming for the file
    for s in ['alpha', 'delta', 'gamma', 'theta', 'beta']:
        if s in path.lower():
            speed_temp = re.findall(r'speed[0-9\.]+', path)
            series = s

            if len(speed_temp) > 0:
                speed = speed_temp[0]

            g_temp = re.findall(r'csf\s[0-9\.]+', path)

            if len(g_temp) > 0:
                g = g_temp[0].replace('csf', '').strip()

                if 'min' in path:
                    name = s + '_' + re.findall(r'[0-9]+min', path)[0]
                else:
                    name = s

                utils.RHYTHMS[name].append((speed, g))

    name = accepted(base.split('.')[0])

    if name is False:
        return base

    if series is not None and speed is not None and g is not None:
        return f'{series}-{speed}-G{g}-{name[-1]}'
    elif series is not None and speed is None and g is None and return_rhythm:
        return f'{series}'

    if name[-1] in ['weight', 'distance', 'tract_length', 'delay', 'speed',
                    'centre', 'area', 'orientation', 'average_orientation', 'normal',
                    'vnormal', 'fnormal', 'sensor', 'volume', 'spike', 'event']:
        if name[-1].endswith('s'):
            return name[-1]
        return name[-1] + 's'
    elif name[-1] == 'fc':
        return 'sim_fc'

    return name[-1]


def accepted(name, return_accepted=False):
    for accept in app.ACCEPTED:
        if accept in name:
            if accept == 'ts' or accept == 'times':
                if accept == 'ts':
                    if '_ts' not in name:
                        return False
                split = name.split('_')
                if len(split) == 2:
                    if return_accepted:
                        return accept
                    return True, split[0] + '_' + split[1]
                if len(split) >= 3:
                    if return_accepted:
                        return accept
                    return True, '_'.join([split[i] for i in range(len(split))])

                if return_accepted:
                    return accept

                return True, accept

            if accept == 'emp' and 'emp_fc' in name:
                if return_accepted:
                    return accept
                return True, 'emp_fc'

            if accept == 'fc' and len(name.split('_')) > 1:
                if return_accepted:
                    return accept
                return False

            if accept != 'ts':
                if return_accepted:
                    return accept
                return True, accept
    return False


def get_filename(path):
    return os.path.basename(path)


def get_file_ext(path):
    return path.split('.')[-1]


def find_separator(path):
    """
    Find the separator/delimiter used in the file to ensure no exception
    is raised while reading files.
    :param path:
    :return:
    """
    if path.split('.')[-1] not in ['txt', 'csv']:
        return

    try:
        file = pd.read_csv(path, index_col=None, header=None, sep=' ')
    except pd.errors.EmptyDataError:
        return 'remove'
    except pd.errors.ParserError:
        file = pd.DataFrame(np.loadtxt(path).tolist())
        os.remove(path)
        file.to_csv(path, header=None, index=None, sep='\t')
    else:
        # if cortical.txt, hemisphere.txt, or areas.txt are present, return '\n' delimiter
        if path.endswith('hemisphere.txt') or path.endswith('cortical.txt') or path.endswith('areas.txt') \
                or path.endswith('times.txt'):
            file.to_csv(path, sep='\n', header=None, index=None)
            return '\n'

        # try with '\t'
        trial = pd.read_csv(path, header=None, sep='\t')
        if trial.shape[0] > 1 and trial.shape[1] > 1:
            return '\t'

        sniffer = csv.Sniffer()

        with open(path) as fp:
            try:
                delimiter = sniffer.sniff(fp.read(5000)).delimiter
            except Exception:
                delimiter = sniffer.sniff(fp.read(50)).delimiter

        delimiter = '\s' if delimiter == ' ' else delimiter
        return delimiter

