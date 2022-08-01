# Coop-robot
This project presents an algorithm that can find a loosing loop in a strategy that moves robot on a ring with the goal to gather them on one point.

## Presentation

This project is the result of a 4 months course and a 2 months intership. It is based on the paper given by my 2 supervisors Nathalie Sznajder and Souheib Baarir, *algorithme_bounded_MC.pdf*. The 2 months intership was based on the *klasing-gathering-07.pdf* report. This report presents a strategy that should allow robots to gather with some constraints on the initial configuration.

What we wanted to do was to test this strategy in the algorithm.

You will find 2 algorithms : 

- One is the *algov5*, it comes from the 4 months course and is related to the *algorithme_bounded_MC.pdf*. We are increasing the size of the loop we are testing as long as we haven't find one.
- The other one, *algov7*, comes from the 2 months intership and has been created by me with the idea that we needed to decrease the time it takes to find a loosing loop and, hopefully one day, the time it takes to find that there is no loosing loop.

## Installation

In order to run and test this algorithm, you will need to install z3 on your computer and not the latest version but the z3-4.7.1 version.

You will find it there : https://github.com/Z3Prover/z3/releases
The version you need was released on May 23th 2018.

Once you have unziped the .tar.gz file, you can install z3 with the python API on your computer. **You need to know your current version of python**. For the following example, I'll use a "python3.5", and the directory "/usr/lib/python3.5/site-packages/" already exists. If it doesn't then create it (cd /usr/lib/python3.5/; mkdir site-packages).

To install z3, from the z3 root directory, execute the following commands :

```bash
python3 scripts/mk_make.py --prefix=/usr --python --pypkgdir=/usr/lib/python3.5/site-packages
```
```bash
cd build
```
```bash
make
```
```bash
sudo make install
```
```bash
sudo echo "export PYTHONPATH=$PYTHONPATH:/usr/lib/python3.5/site-packages" >> ~/.bashrc
```

From the root directory of this project (Coop-robot):

```bash
cat scripts/ajoutException.patch > /usr/lib/python3.5/site-packages/z3/ajoutException.patch
```
```bash
sudo patch -d /usr/lib/python3.5/site-packages/z3/ < /usr/lib/python3.5/site-packages/z3/ajoutException.patch
```

Once you've done all that, restart your shell and you are ready to use the z3 API.

## Use

