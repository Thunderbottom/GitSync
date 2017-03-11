# GitSync

Python script to sync GitHub repositories with your machine.
The script is currently in its initial stages, and the code isn't really clean, so the functioning *might* vary depending on the machine it is running on.



## Usage

```
usage: syncrepo.py [-h] [--no-skip-forks] [--directory DIRECTORY]
                   [---lang-dir] [--commit-all]

optional arguments:
  -h, --help              show this help message and exit.
  --no-skip-forks, -ns    Skips if the current repository is a fork
  --directory DIRECTORY,  Set location for sync. If not set, cwd/GitSync/ is used.  
  -d DIRECTORY
  ---lang-dir, -ld        Segregate git project folders by language (May or may
                          not work with existing projects).
  --commit-all, -c        Commit everything to the current git repository.
                          Add commit.txt with commit message to every git repo directory.
                          Requests user for commit message if the txt file is not found.                        
```


## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D



## History

**2017-03-11** - *Initial Release*
  * Sync all git repositories to your machine
  * Segregate repositories by their languages
  * Batch commit changes to your profile
  * Remote sync and update fork
  * Option to ignore fork sync



## TODO

  * Clean up code
  * Allow user to sync only select repositories



## Credits

  * [@MSV-Jarvis](https://github.com/MSF-Jarvis)



## License

```License
MIT License

Copyright (c) 2017 Chinmay Pai

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
