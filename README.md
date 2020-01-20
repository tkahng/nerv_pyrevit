# Nerv_pyRevit

This is a repository for Autodesk Revit incorporating various useful tools used in professional work. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* [Autodesk Revit](https://www.autodesk.com/products/revit/overview) 
* [pyRevit](https://github.com/eirannejad/pyRevit)

### Installing

1. Please clone or download the repository and unzip to your desired location.
2. Go to your pyRevit toolbar(must have pyRevit installed) and add the unzipped location to the 'Custom Extension Directories'.
3. Click the 'Save Settings and Reload' 
4. A custom toolbar should appear in your Revit, please ignore any warnings because the tool is still under development.


## Deployment

Deployment and update on a large scale is recommended by using a server based read only location for the location to host this repository. Use a .bat file or any other desired methods in the background to modify the ini file located in each user's Revit Plugin Folder:

Autodesk Revit addins are generally loaded from the following locations. 
```
User Addins:
%appdata%\Autodesk\Revit\Addins\

Machine Addins (for all users of the machine):
C:\ProgramData\Autodesk\Revit\Addins\

Addins packaged for the Autodesk Exchange store:
C:\ProgramData\Autodesk\ApplicationPlugins\

Autodesk servers and services:
C:\Program Files\Autodesk\Revit 2016\AddIns\
```
## Built With

* [Autodesk Revit](https://www.autodesk.com/products/revit/overview) 
* [pyRevit](https://github.com/eirannejad/pyRevit)
* [IronPython](https://ironpython.net/)


## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us. Please contact loumengfan@gmail.com to get permission. 

## Versioning

This project will use [SemVer](http://semver.org/) for versioning after all milestones are complete. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Mengfan Lou** - *Author* - [lmengfan](https://github.com/lmengfan)


## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](https://github.com/lmengfan/Nerv_pyRevit/blob/master/LICENSE) file for details

## Acknowledgments

* [Ehsan Iran-Nejad](https://github.com/eirannejad) This work is mostly based on his work on pyRevit.
* [Revit API docs](https://www.revitapidocs.com/) Revit API documentation site is used for reference.
* [Gui Talarico](https://github.com/gtalarico) Revit Python Wrapper Library.
* [Daren Thomas](https://github.com/daren-thomas) Revit Python Shell was used for most of the testing work.
