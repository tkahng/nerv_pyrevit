# PyRevit_Custom_Tools

This is a repository for Autodesk Revit incorporating various useful tools used in professional work. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```
# PyRevit_Custom_Tools

This is a repository for Autodesk Revit incorporating various useful tools used in professional work. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

1. Must have Autodesk Revit installed.
2. Must have pyRevit plugin for Revit installed.

### Installing

1. Please clone or download the repository and unzip to your desired location.
2. Go to your pyRevit toolbar(must have pyRevit installed) and add the unzipped location to the 'Custom Extension Directories'.
3. Click the 'Save Settings and Reload' 
4. A custom toolbar should appear in your Revit, please ignore any warnings because the tool is still under development.

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Deployment and update on a large scale is recommended by using a server based read only location for the location to host this repository. Use a .bat file or any other desired methods in the background to modify the ini file located in each user's Revit Plugin Folder:

Autodesk Revit addins are generally loaded from the following locations. 

User Addins:
%appdata%\Autodesk\Revit\Addins\

Machine Addins (for all users of the machine):
C:\ProgramData\Autodesk\Revit\Addins\

Addins packaged for the Autodesk Exchange store:
C:\ProgramData\Autodesk\ApplicationPlugins\

Autodesk servers and services:
C:\Program Files\Autodesk\Revit 2016\AddIns\

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
