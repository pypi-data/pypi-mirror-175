import json
import os
import re
from collections import OrderedDict

import pandas as pd

from sim2bids.app import app
from sim2bids.generate import subjects
import sim2bids.templates.templates as temp

# define naming conventions
DEFAULT_TEMPLATE = '{}_{}.{}'
COORD_TEMPLATE = '{}.{}'

# set to true if centres.txt (nodes and labels) are the same
# for all files. In that case, store only one copy of the files
# (json, tsv) in the main 'coord' folder, in the global scope
IGNORE_CENTRE = False
IGNORE_AREAS = False
IGNORE_CORTICAL = False
IGNORE_HEMISPHERE = False
IGNORE_NORMALS = False

# location of coord files (nodes and labels) in the scope of
# converted files. This information is used to supplement JSON
# sidecars, specifically `CoordsRows` and `CoordsColumns`
COORDS = None

# set true if `times` are the same for all files. In that case,
# store only one copy of the files (json, tsv) in the main 'coord'
# folder, in the global scope
IGNORE_TIMES = False

NETWORK = []
TIMES_TO_SKIP = []


def save(sub: dict, folders: list, ses: str = None, name: str = None) -> None:
    """Main engine to save all conversions. Several functionalities to understand:

    1. Check all centres files to see if they have identical content. If so,
       only one copy gets saved in the main area of the output folder (by default
       this folder is in root level of the project in 'output' folder), specifically,
       in 'coord' folder. The same structure is applied for single-subject inputs.
       The final structure will have the following layout:
                            |__ output
                                |__ coord
                                    |__ desc-<label>_<suffix>.json
                                    |__ desc-<label>_<suffix>.tsv

       Otherwise, if input data has multi-subject files, the 'coord' folder will be
       deleted in the root-level. The final structure will have the following layout:
                            |__ output
                                |__ sub-<ID>
                                    |__ coord
                                        |__ sub-<ID>_desc-<label>_<suffix>.json
                                        |__ sub-<ID>_desc-<label>_<suffix>.tsv

       To overcome redundancy, the first run will happen as usual; it will check all
       centres files and update the global parameter IGNORE_CENTRE. This argument indicates
       whether the following centres should be omitted or not. If true, the function will
       immediately break. Otherwise, all centres will be stored in their respective folders.

    2. Read file contents. This is pretty straight-forward, given a file location,
       the app gets its contents. Supported file types are '.txt', '.csv', '.dat', '.mat',
       and '.h5'.

       Tips:
            1. Make sure to have 1 (!) array in MATLAB (.mat), HDF5 (.h5) files. If there
               are multiple arrays, the app will ignore them.
            2. Make sure to store textual data (e.g., 'lh_bankssts') in the first column (!)
               of 'centres.txt' file. When 'centres.txt' file is passed, the app divides its
               columns to labels (Nx1, 1st column) and nodes (NxN-1, 2nd-Nth column). If you
               have nodes and labels separated in 'nodes.txt' and 'labels.txt' files, you
               can safely ignore this information.

    3. Get folder locations. Depending on the passed file, get its respective folder location.

    4. Save files.

    Parameters
    ----------
    sub (dict):
        Dictionary containing information of one file only. For example,
        {'name': 'centres', 'fname': 'centres.txt', 'sid': '1', 'desc': 'default',
        'sep': '\t', 'path': PATH_TO_FILE, 'ext': 'txt'}
    folders (list):
        List of folders corresponding to whether input files have single- or
        multi-subject, or session-based structure. Each structure contains a
        different sequence of folders created in 'app.py' in 'create_sub_struct' function.
    ses (str):
        Session type (ses-preop, ses-postop, None). If sessions are present,
        appropriate files are stored in their appropriate session folders.
        Otherwise, the structure follows the standard layout.
    name (str):
        Name of the file. Accepted names:
            'weight', 'distance', 'tract_length', 'delay', 'speed',                 # Network (net)
            'nodes', 'labels', 'centres', 'area', 'hemisphere', 'cortical',         # Coordinates (coord)
            'orientation', 'average_orientation', 'normal', 'times', 'vertices',    # Coordinates (coord)
            'faces', 'vnormal', 'fnormal', 'sensor', 'map', 'volume',               # Coordinates (coord)
            'cartesian2d', 'cartesian3d', 'polar2d', 'polar3d',                     # Coordinates (coord)
            'vars', 'stimuli', 'noise', 'spike', 'raster', 'ts', 'event', 'emp'     # Timeseries (ts)
            'fc'                                                                    # Spatial (spatial)
    """
    global IGNORE_CENTRE, IGNORE_CORTICAL, IGNORE_AREAS, IGNORE_NORMALS, IGNORE_HEMISPHERE

    # if name == 'centres' and sub['name'] not in ['nodes', 'labels']:
    #     name = 'coord'

    # check if centres should be ignored. If so, immediately break
    # the function. Otherwise, continue iteration.
    if IGNORE_CENTRE is True and name == 'centres' and os.path.exists(os.path.join(app.OUTPUT, 'coord', 'nodes.txt')):
        return

    # read file contents
    file = open_file(sub['path'], sub['sep'])

    # get folder location for weights and distances
    if name == 'wd':
        # set appropriate output path depending on session type
        if ses is None:
            folder = folders[1]
        else:
            folder = folders[2]

        # get description for weights or distances
        if 'scthran' in sub['name'].lower():
            desc = temp.file_desc['weights'].format('thresholded ')
        elif 'scnot' in sub['name'].lower():
            desc = temp.file_desc['weights'].format('')
        else:
            desc = temp.file_desc['distances']

        if 'content' in sub.keys():
            save_files(sub, folder, sub['content'], ftype='wd')
        else:
            # save conversion results
            save_files(sub, folder, file, desc=desc, ftype='wd')

    # get folder location for centres
    elif name == 'centres':
        save_centres(sub, file, ses, folders)

    # get folder location for spatial
    elif name in ['spatial', 'fc', 'map']:
        fname = subjects.accepted(sub['name'], True)
        desc = temp.file_desc['spatial_map'] if 'map' in fname \
               else temp.file_desc[subjects.accepted(fname, return_accepted=True)].format(sub['sid'])

        if ses is None:
            folder = folders[2]
        else:
            folder = folders[3]

        if 'content' in sub.keys():
            save_files(sub, folder, sub['content'], type='default', ftype='spatial', desc=desc)
        else:
            # save conversion results
            save_files(sub, folder, file, type='default', ftype='spatial', desc=desc)

    # get folder location for time series
    elif name in ['ts']:
        desc = temp.file_desc['ts'].format(sub['sid']) if name == 'ts' else temp.file_desc['bold'].format(sub['sid'].replace('sub-', ''))
        save_files(sub, folders[-1], file, type='default', ftype='ts', desc=desc)

    elif name == 'times':
        traverse_times(sub, folders, ses)

    # get folder location for coordinates
    elif name == 'coord':
        # check nodes
        if ('nodes' in sub['name'] or 'labels' in sub['name']) and not IGNORE_CENTRE:
            if 'content' in sub.keys():
                save_centres(sub, sub['content'], ses, folders, centre_name='nodes')
            else:
                save_centres(sub, file, ses, folders, centre_name='nodes')
        else:
            # set naming convention needed for conversion
            type_ = 'default'

            # set appropriate output path depending on session and subject types
            if ses is not None:
                folder = folders[4]
            elif app.MULTI_INPUT and ses is None:
                folder = folders[3]
            else:
                folder = os.path.join(app.OUTPUT, 'coord')

            # check contents of areas
            if 'areas' in sub['path']:
                if IGNORE_AREAS is True:
                    return
                IGNORE_AREAS = check_file('areas', sub, folder, file)

            # check contents of cortical
            elif 'cortical' in sub['path']:
                if IGNORE_CORTICAL is True:
                    return
                IGNORE_CORTICAL = check_file('cortical', sub, folder, file)

            # check contents of cortical
            elif 'normals' in sub['path']:
                if IGNORE_NORMALS is True:
                    return
                IGNORE_NORMALS = check_file('normals', sub, folder, file)

            # check contents of cortical
            elif 'hemisphere' in sub['path']:
                if IGNORE_HEMISPHERE is True:
                    return
                IGNORE_HEMISPHERE = check_file('hemisphere', sub, folder, file)
            else:
                accepted = subjects.get_name(sub['name'], True)

                if app.SESSIONS:
                    save_files(sub, folder, file, type='default', desc=temp.file_desc[accepted])
                # elif IGNORE_CENTRE and 'ses' not in folder and app.SESSIONS is None:
                elif IGNORE_CENTRE and not app.SESSIONS:
                    save_files(sub, folder, file, type='other', desc=temp.file_desc[accepted])
                else:
                    accepted = subjects.get_name(sub['name'])

                    if IGNORE_CENTRE and 'sub' in folder:
                        type_ = 'default'
                    else:
                        type_ = 'coord'

                    save_files(sub, folder, file, type=type_, desc=temp.file_desc[accepted])


            #
            # if 'content' in sub.keys():
            #     save_files(sub, folder, file, type='default', centres=True)
            # else:
            #     if sub['name'] in ['nodes', 'labels']:
            #         save_centres(sub, file, ses, folders)
            #
            #     # save conversion results
            #     if 'centres' in sub['fname']:
            #         if IGNORE_CENTRE or not app.MULTI_INPUT:
            #             save_files(sub, folder, file, type='other', centres=True, desc=temp.centres['single'])
            #         else:
            #             save_files(sub, folder, file, type='default', centres=True, desc=temp.centres['multi-unique'])
            #     else:
            #         accepted = subjects.get_name(sub['name'], True)
            #
            #         if app.SESSIONS:
            #             save_files(sub, folder, file, type='default', desc=temp.file_desc[accepted])
            #         # elif IGNORE_CENTRE and 'ses' not in folder and app.SESSIONS is None:
            #         elif IGNORE_CENTRE and not app.SESSIONS:
            #             save_files(sub, folder, file, type='other', desc=temp.file_desc[accepted])
            #         else:
            #             accepted = subjects.get_name(sub['name'])
            #
            #             if IGNORE_CENTRE and 'sub' in folder:
            #                 type_ = 'default'
            #             else:
            #                 type_ = 'coord'
            #
            #             save_files(sub, folder, file, type=type_, desc=temp.file_desc[accepted])


def check_file(name, sub, folder, file):
    if check_coords(name):
        save_files(sub, os.path.join(app.OUTPUT, 'coord'), file, type='other', desc=temp.file_desc[name])
        return True

    save_files(sub, folder, file, type='default', desc=temp.file_desc[name])
    return False


def save_centres(sub, file, ses, folders, centre_name='centres'):
    global IGNORE_CENTRE

    # check if all centres are of the same content
    if check_coords(name=centre_name):
        # ignore preceding centres files
        IGNORE_CENTRE = True

        # set output path to store coords in
        folder = os.path.join(app.OUTPUT, 'coord')

        # save conversion results
        save_files(sub, folder, file, type='other', centres=True, desc=temp.centres['multi-same'])
    else:
        # get description for centres depending on input files
        desc = temp.centres['multi-unique'] if app.MULTI_INPUT else temp.centres['single']

        # set appropriate output path depending on session and subject types
        if len(folders) > 1:
            if ses is not None:
                folder = folders[4]
            elif app.MULTI_INPUT and ses is None:
                folder = folders[3]
            else:
                folder = os.path.join(app.OUTPUT, 'coord')
        else:
            folder = folders[0]

        # save conversion results
        if IGNORE_CENTRE:
            save_files(sub, folder, file, type='other', centres=True, desc=desc)
        else:
            save_files(sub, folder, file, type='default', centres=True, desc=desc)


def save_h5(sub, folders, ses=None):
    pass


def save_files(sub: dict, folder: str, content, type: str = 'default', centres: bool = False,
               desc: [str, list, None] = None, ftype: str = 'coord'):
    """
    This function prepares the data to be stored in JSON/TSV formats. It first creates
    absolute paths where data is to be stored, deals with 'centres.txt' file and
    preprocesses it. Then, sends the finalized versions to the function that
    saves JSON and TSV files.

    Parameters
    ----------
    sub (dict):
        Dictionary containing information of one file only. For example,
        {'name': 'centres', 'fname': 'centres.txt', 'sid': '1', 'desc': 'default',
        'sep': '\t', 'path': PATH_TO_FILE, 'ext': 'txt'}
    folder (str):
        Folder where to store output conversions for the specific file. For example,
        if the passed file is 'weights.txt' and the input files have both sessions and
        multi-subject structure, then 'weights.txt' will be stored like:
                            |__ output
                                |__ sub-<ID>
                                    |__ ses-preop
                                        |__ net
                                            |__ sub-<ID>_desc-<label>_weights.json
                                            |__ sub-<ID>_desc-<label>_weights.tsv
    content (pd.DataFrame, np.array, ...)
        Content of the specific file.
    type (str):
        Type of default name to use. There are two options: default and coordinate.
        The first creates the following file name:
                                sub-<ID>_desc-<label>_<suffix>.json|.tsv
        The other creates the following file name (basically, omitting the ID):
                                    desc-<label>_<suffix>.json|.tsv
    centres (bool):
        Whether the file is 'centres.txt'. Centres require additional treatment as
        splitting the folder into 'nodes.txt' and 'labels.txt', therefore, it should
        be distinguished from others.
    desc (str):
        Description of the file; this information will be added to the JSON sidecar.
    ftype (str):
        File type of the passed file. Accepted types:
            'wd' (weights and distances), 'coord' (coordinate), 'ts' (time series),
            'spatial', 'eq' (equations), 'param' (parameters), and 'code'.
    """
    global COORDS

    name = sub['name'].replace('.txt', '')

    if type == 'default':
        json_file = os.path.join(folder, DEFAULT_TEMPLATE.format(sub['sid'], name, 'json'))
        tsv_file = json_file.replace('json', 'tsv')

    else:
        json_file = os.path.join(folder, COORD_TEMPLATE.format(name, 'json'))
        tsv_file = json_file.replace('json', 'tsv')

    # Save 'centres.txt' as 'nodes.txt' and 'labels.txt'. This will require breaking the
    # 'centres.txt' file, the first column HAS TO BE labels, and the rest N dimensions
    # are nodes.
    if centres:
        # create names for nodes and labels
        # Since the usual structure leaves the name of the files as is,
        # we need to make sure we save 'nodes' and 'labels' appropriately.
        # If we didn't create these two values below, both labels and nodes
        # would be stored as 'sub-<ID>_desc-<label>_centres.txt', and the
        # content would only have nodes.
        labels = json_file.replace(sub['name'], 'labels')
        nodes = json_file.replace(sub['name'], 'nodes')

        if COORDS is None:
            if IGNORE_CENTRE or not app.MULTI_INPUT:
                COORDS = [f'../coord/desc-{app.DESC}_labels.json', f'../coord/desc-{app.DESC}_nodes.json']
            else:
                COORDS = [labels.replace(app.OUTPUT, '../..').replace('\\', '/'),
                          nodes.replace(app.OUTPUT, '../..').replace('\\', '/')]

        # save labels to json and tsv
        to_json(labels, shape=[content.shape[0], 1], key='coord', desc=desc[0])
        to_tsv(labels.replace('json', 'tsv'), content.iloc[:, 0])

        # save nodes to json and tsv
        to_json(nodes, shape=[content.shape[0], content.shape[1] - 1], key='coord', desc=desc[1])
        to_tsv(nodes.replace('json', 'tsv'), content.iloc[:, 1:])
    else:
        if ftype == 'coord':
            to_json(json_file, shape=content.shape, key='coord', desc=desc)
            to_tsv(tsv_file, content)
        else:
            # otherwise, save files as usual
            to_json(json_file, shape=content.shape, key=ftype, desc=desc)
            to_tsv(tsv_file, content)


def check_coords(name='centres'):
    """
    This function checks all centres files in the input folder and
    decides whether they have the same content or not. The logic of
    this functionality is the following, we take the first arbitrary
    centres.txt file and compare it to the rest. We don't check every
    single centres file against the rest. Thus, only one checking round
    happens here.

    It's important to note that if users pass in 2+ subject folders and only
    one contains centres.txt, the 'coord' folder is created for one subject only.
    """

    # get all centres files
    files = get_specific(name)

    if len(files) == 1:
        return True

    if files:
        # get the first element
        f1 = open_file(files[0], subjects.find_separator(files[0]))
        f2 = open_file(files[1], subjects.find_separator(files[1]))

        if f1.equals(f2):
            return True
        return False

    return False


def get_specific(filetype: str, constraint: str = None) -> list:
    """
    Get all files that correspond to the filetype. For example,
    if filetype is equal to "areas", this function will return
    all files containing that keyword.

    Parameters
    ----------
    filetype: str
        Type of the file to search for. Accepted types:
            'weight', 'distance', 'tract_length', 'delay', 'speed',                 # Network (net)
            'nodes', 'labels', 'centres', 'area', 'hemisphere', 'cortical',         # Coordinates (coord)
            'orientation', 'average_orientation', 'normal', 'times', 'vertices',    # Coordinates (coord)
            'faces', 'vnormal', 'fnormal', 'sensor', 'map', 'volume',               # Coordinates (coord)
            'cartesian2d', 'cartesian3d', 'polar2d', 'polar3d',                     # Coordinates (coord)
            'vars', 'stimuli', 'noise', 'spike', 'raster', 'ts', 'event', 'emp'     # Timeseries (ts)
            'fc'                                                                    # Spatial (spatial)

    Returns
    -------
        Returns a list of all files that end with the specified filetype.
        :param constraint:
    """

    # create emtpy list to store appropriate files
    content = []

    # iterate over all files found by the app previously
    for file in app.ALL_FILES:
        # check if the keyword is present
        if filetype in file:
            if constraint is not None and constraint in file:
                content.append(file)
            if constraint is None:
                # if yes, append the value
                content.append(file)

    # return the list of newly-found files
    return content


def open_file(path: str, sep: str):
    """

    Parameters
    ----------
    path :
        param sep:
    path: str :

    sep: str :


    Returns
    -------

    """

    ext = path.split('.')[-1]

    if ext in ['txt', 'csv', 'dat']:
        return open_text(path, sep)

    elif ext == 'mat':
        pass

    elif ext == 'h5':
        pass


def traverse_times(sub, folders, ses):
    global TIMES_TO_SKIP

    # get description
    desc = temp.file_desc['times'] if 'bold' not in sub['name'] else temp.file_desc['bold_times']

    # check if times are similar
    for times in app.TIMES:
        for rhythm in ['alpha', 'delta', 'beta', 'gamma', 'theta']:
            # check if the file needs to be skipped
            if f'{rhythm}_{times}' in TIMES_TO_SKIP:
                return

            results = get_specific(times, rhythm)

            if len(results) > 0:
                open_df = lambda x: pd.read_csv(x, header=None, sep='\t')
                first = open_df(results[0])

                if len(results) > 1:
                    for result in results[1:]:
                        if first.equals(open_df(result)):
                            similar = True
                            TIMES_TO_SKIP.append(f'{rhythm}_{times}')

                            # save in global folder
                            sub['name'] = f'{rhythm}-{times}'
                            save_files(sub, os.path.join(app.OUTPUT, 'coord'), first, 'coord', desc=desc)
                        else:
                            # set appropriate output path depending on session and subject types
                            if ses is not None:
                                folder = folders[4]
                            elif app.MULTI_INPUT and ses is None:
                                folder = folders[3]
                            else:
                                folder = os.path.join(app.OUTPUT, 'coord')

                            save_files(sub, folder, first, 'default', desc=desc)
                            save_files(sub, folder, open_df(result), 'default', desc=desc)
                else:
                    similar = True
                    TIMES_TO_SKIP.append(f'{rhythm}_{times}')
                    # save in global folder
                    sub['name'] = f'{rhythm}-{times.replace(".txt", "")}'
                    save_files(sub, os.path.join(app.OUTPUT, 'coord'), first, 'coord', desc=desc)


def open_text(path, sep):
    """

    Parameters
    ----------
    path :
        param sep:
    sep :


    Returns
    -------

    """
    if sep == '\n':
        return pd.read_csv(path, header=None, index_col=None)

    try:
        f = pd.read_csv(path, sep=sep, header=None, index_col=None)
    except pd.errors.EmptyDataError:
        return ''
    except ValueError:
        return ''
    else:
        return f


def to_tsv(path, file, sep=None):
    """

    Parameters
    ----------
    path :
        param file:
    sep :
        return: (Default value = None)
    file :


    Returns
    -------

    """
    params = {'sep': '\t', 'header': None, 'index': None}
    sep = sep if sep != '\n' else '\0'

    if isinstance(file, str) and sep is not None:
        pd.read_csv(file, index_col=None, header=None, sep=sep).to_csv(path, **params)
    else:
        try:
            pd.DataFrame(file).to_csv(path, **params)
        except ValueError:
            with open(file) as f:
                with open(path, 'w') as f2:
                    f2.write(f.read())


def to_json(path, shape, desc, key, **kwargs):
    """

    Parameters
    ----------
    path :
        param shape:
    desc :
        param key:
    kwargs :
        return:
    shape :

    key :

    **kwargs :


    Returns
    -------

    """
    global NETWORK

    if key not in ['param', 'eq', 'code']:
        out = OrderedDict({x: '' for x in temp.required})
    else:
        out = OrderedDict()

    if key != 'wd':
        struct = temp.struct[key]
        out.update({x: '' for x in struct['required']})

    # ===========================================================
    #                     TAKE CARE OF COORDS
    # ===========================================================
    coord = None

    if 'CoordsRows' in out.keys() or key in ['wd', 'ts', 'spatial']:
        if app.SESSIONS and IGNORE_CENTRE:
            coord = ['../../../coord/nodes.json', '../../../coord/labels.json']
        elif app.SESSIONS and not IGNORE_CENTRE:
            coord = ['../coord/nodes.json', '../coord/labels.json']
        elif not app.SESSIONS and IGNORE_CENTRE:
            coord = ['../../coord/nodes.json', '../../coord/labels.json']
        else:
            coord = ['../coord/nodes.json', '../coord/labels.json']

    if key != 'wd':

        # ===========================================================
        #                     TAKE CARE OF EQUATIONS
        # ===========================================================

        if 'ModelEq' in out.keys() or 'ModelEq' in temp.struct[key]['recommend']:
            if 'param' in path or 'code' in path:
                out['ModelEq'] = '../eq/eq.xml'
            else:
                if app.SESSIONS:
                    out['ModelEq'] = '../../../eq/eq.xml'
                else:
                    out['ModelEq'] = '../../eq/eq.xml'

        # ===========================================================
        #                     TAKE CARE OF PARAMETERS
        # ===========================================================

        if 'ModelParam' in out.keys() or 'ModelParam' in temp.struct[key]['recommend']:
            if 'eq' in path or 'code' in path:
                out['ModelParam'] = '../param/param.xml'
            else:
                if app.SESSIONS:
                    out['ModelParam'] = '../../../param/param.xml'
                else:
                    out['ModelParam'] = '../../param/param.xml'

        params = {
            'SourceCode': f'/tvb-framework-{app.SoftwareVersion}' if app.SoftwareCode == 'MISSING' else app.SoftwareCode,
            'SoftwareVersion': app.SoftwareVersion if app.SoftwareVersion else None,
            'SoftwareRepository': app.SoftwareRepository if app.SoftwareRepository else None,
            'SourceCodeVersion': app.SoftwareVersion if app.SoftwareVersion else None,
            'SoftwareName': app.SoftwareName if app.SoftwareName else None,
            'Network': NETWORK if NETWORK else None
        }

        if 'eq' not in path or 'param' not in path or 'code' not in path:
            sub = re.findall(r'sub-[0-9]+', path)
            network = None

            if sub:
                network = [f'../net/{sub[0]}_{app.DESC}_weights.json', f'../net/{sub[0]}_{app.DESC}_distances.json']

            if network:
                params['Network'] = network

        if kwargs:
            params += kwargs

        for k in params.keys():
            if k in temp.struct[key]['required'] or k in temp.struct[key]['recommend']:
                out[k] = params[k]

    if 'Units' in out.keys():
        if key == 'wd' or key == 'coord':
            out['Units'] = ''
        else:
            out['Units'] = 'ms'

    with open(path, 'w') as file:
        json.dump(temp.populate_dict(out, shape=shape, desc=desc, coords=coord), file)
