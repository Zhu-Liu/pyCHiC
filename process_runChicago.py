#!/usr/bin/env python

"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from __future__ import print_function

#Required for ReadTheDocs
from functools import wraps

import argparse

from basic_modules.workflow import Workflow
from utils import logger

from tool.runChicago import ChicagoTool

#################################################

class process_Chicago(Workflow):
    """
    Function for processing capture Hi-C fastq files. Files are aligned,
    filtered and analysed for Cpature Hi-C peaks
    """

    def __init__(self, configuration=None):
        """
        initiate the class

        Parameters:
        -----------
        Configuration: dict
        dictinoary with parameters for different Tools, indicating
        how to run each of them
        """

        logger.info("Processing chicago")
        if configuration==None:
            configuration = {}

        self.configuration.update(configuration)

    def run(self, input_files, input_metadata, output_files):
        """
        This main function that run the chicago pipeline with runChicago.R wrapper

        Parameters:
        -----------

        input_files: dict
            location with the .chinput files.
                chinput_file: str in case there is one input file
                chinput_file: comma separated list in case there
                    is more than one input file.

        metadata: dict
                Input metadata, str

        output: dict
            output file locations

        Returns
        --------

        output_files : dict
            Folder location with the output files

        output_metadata: dict
            Output metadata for the associated files in output_files
        """

        output_files_generated = {}
        output_metadata = {}

        logger.info("Process chicago - defined output:", output_files)

        #chicago
        chicago_caller = ChicagoTool(self.configuration)
        output_files_generated, output_metadata = chicago_caller.run(
            {
                "chinput_file" : input_files["chinput_file"],
            }, {
                "chinput_1" : input_metadata["chinput_1"],
                "chinput_2" : input_metadata["chinput_2"]
            }, {
                "output_prefix" : output_files["output_prefix"],
                "output_dir" : output_files["output_dir"]
            }
        )

        print("chicago results: ", output_metadata)
        return output_files_generated, output_metadata


################################################################

def main_json(config, in_metadata, out_metadata):
    """
    Alternative main function

    This function launches the app using configuration written in
    two json files: config.json and input_metadata.json
    """

    # 1. Instantiate and launch the App
    print("1. Instantiate and launch the App")
    from apps.jsonapp import JSONApp
    app = JSONApp()
    results = app.launch(process_Chicago,
                         config,
                         in_metadata,
                         out_metadata)

    # 2. The App has finished
    print("2. Execution finished; see " + out_metadata)
    print(results)

    return results

###############################################################

if __name__ == "__name__":

    #set up the command line parameters
    PARSER = argparse.ArgumentParser(
        description= "Chicago algorithm for capture Hi-C peak detection")

    PARSER.add_argument("--config", help="Configuration file")
    PARSER.add_argument(
        "--in_metadata", help= "Location of metadata file")
    PARSER.add_argument(
        "--out_metadata", help="Location of output metadata file")
    PARSER.add_argument(
        "--local", action="store_const", cont=True, default=False)

    #Get matching parameters from the command line
    ARGS = PARSER.parse_args()

    CONFIG = ARGS.config
    IN_METADATA = ARGS.in_metadata
    OUT_METADATA = ARGS.out_metadata
    LOCAL = ARGS.local

    if LOCAL:
        import sys
        sys._run_from_cmdl = True

    RESULTS = main_json(CONFIG, IN_METADATA, OUT_METADATA)

    print(RESULTS)



















