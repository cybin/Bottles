import os
import hashlib


class Diff:

    def __hashify(self, path: str) -> dict:
        '''
        Hash (SHA-1) all files in a directory and return
        them in a dictionary. Here we use SHA-1 instead of
        better ones like SHA-256 because we only need to
        compare the file hashes, it's faster and it's
        not a security risk.
        '''
        _files = {}

        if path[-1] != os.sep:
            '''
            Be sure to add a trailing slash at the end of the path to
            prevent the correct path name in the result.
            '''
            path += os.sep

        for root, dirs, files in os.walk(path):
            for f in files:
                if "dosdevices" in root or "users" in root:
                    '''
                    Skip the dosdevices and users folders as these
                    generate loops due to symlinks, also these are
                    not relevant for layers.
                    '''
                    continue
                with open(os.path.join(root, f), "rb") as fr:
                    _hash = hashlib.sha1(fr.read()).hexdigest()
                
                _key = os.path.join(root, f)
                _key = _key.replace(path, "")
                _files[_key] = _hash
        
        return _files

    def compare(self, parent: str, child: str) -> dict:
        '''
        Compare two directories and return a dictionary
        with the differences (added, removed, changed).
        '''
        _parent = self.__hashify(parent)
        _child = self.__hashify(child)
        
        added = []
        removed = []
        changed = []
        
        for f in _child:
            if f not in _parent:
                added.append(f)
            elif _parent[f] != _child[f]:
                changed.append(f)
        
        for f in _parent:
            if f not in _child:
                removed.append(f)
        
        return {
            "added": added, 
            "removed": removed, 
            "changed": changed
        }