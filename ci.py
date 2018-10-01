#!/usr/bin/python3
import os
from argparse import ArgumentParser
from dind import Pipeline

dirPath = os.path.dirname(os.path.realpath(__file__))
pipeline = Pipeline(dockerRegistry='registry.gitlab.com/christiantragesser')
localTag = 'local/yadi'
latestTag = 'registry.gitlab.com/christiantragesser/yadi-py:latest'

def ci(option):
    stage = {
        'test': test,
        'scan': securityScan,
        'local': local,
        'qa': qa
    }
    run = stage.get(option, test)
    run()

def test():
    testDir = '/tmp/test'
    volumes = {
        dirPath: { 'bind': '/tmp', 'mode': 'rw'}
    }
    cleanMe = []
    print('Starting tests:')
    pipeline.buildImage(dirPath, localTag)
    cleanMe.append(pipeline.runContainerDetached(image=localTag, name='yadi'))
    pipeline.runContainerInteractive(image='registry.gitlab.com/christiantragesser/dind-py:3',
                                     name='yadi-test', working_dir=testDir, volumes=volumes, command='pytest')
    pipeline.purgeContainers(cleanMe)
    print('Testing complete')

def securityScan():
    print('Starting security scans:')
    pipeline.cveScan(localTag)

def local():
    print('Initializing locally built instance:')
    port = { 5000: 5000 }
    pipeline.buildImage(dirPath,localTag)
    pipeline.runContainerDetached(image=localTag, ports=port, name='yadi')

def qa():
    print('Starting yadi:')
    port = { 5000: 5000 }
    pipeline.runContainerDetached(image=latestTag, ports=port, name='yadi')

def main():
    parser = ArgumentParser(prog='ci-py')
    parser.add_argument('stage', type=str,
                        help='run pipeline stage; test, scan, local, qa')
    args = parser.parse_args()
    ci(args.stage)

if __name__ == '__main__':
    main()