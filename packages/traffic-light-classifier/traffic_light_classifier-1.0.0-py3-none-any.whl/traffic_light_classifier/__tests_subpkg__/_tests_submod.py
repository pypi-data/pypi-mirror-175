
# ==================================================================================================================================
# START >> FILE INFO
# ==================================================================================================================================
# File        : traffic_light_classifier/__tests_subpkg__/_tests_submod.py
# Author      : Shashank Kumbhare
# Date        : 09/20/2022
# email       : shashankkumbhare8@gmail.com
# Description : This file is a python submodule for python subpackage
#               'traffic_light_classifier.__tests_subpkg__'.
# ==================================================================================================================================
# END << FILE INFO
# ==================================================================================================================================



# ==================================================================================================================================
# START >> SUBMODULE >> traffic_light_classifier.__tests_subpkg__._tests_submod
# ==================================================================================================================================
# >>
"""
This submodule contains tools to perform unittests on the functionalities of the
package.
"""



# ==================================================================================
# START >> IMPORTS
# ==================================================================================
# >>
from ..__dependencies_subpkg__ import *
from ..__constants_subpkg__    import *
from ..__auxil_subpkg__        import *
from ..__data_subpkg__         import *
# <<
# ==================================================================================
# END << IMPORTS
# ==================================================================================


# ==================================================================================
# START >> EXPORTS
# ==================================================================================
# >>
__all__ = ["Tests"]
# <<
# ==================================================================================
# END << EXPORTS
# ==================================================================================


# ==================================================================================================================================
# START >> CLASS >> Tests
# ==================================================================================================================================
# >>
class Tests(unittest.TestCase):
    
    """
    A class holding all tests.
    """
    
    # Tests the `one_hot_encode` function, which is passed in as an argument
    def test_one_hot(self, one_hot_function):
        
        # Test that the generated one-hot labels match the expected one-hot label
        # For all three cases (red, yellow, green)
        try:
            self.assertEqual([1,0,0], one_hot_function('red'))
            self.assertEqual([0,1,0], one_hot_function('yellow'))
            self.assertEqual([0,0,1], one_hot_function('green'))
        
        # If the function does *not* pass all 3 tests above, it enters this exception
        except self.failureException as e:
            # Print out an error message
            print_fail()
            print("Your function did not return the expected one-hot label.")
            print('\n'+str(e))
            return
        
        # Print out a "test passed" message
        print_pass()
    
    # Tests if any misclassified images are red but mistakenly classified as green
    def test_red_as_green(self, misclassified_images):
        # Loop through each misclassified image and the labels
        for im, predicted_label, true_label in misclassified_images:
            
            # Check if the image is one of a red light
            if true_label == [1,0,0]:
                
                try:
                    # Check that it is NOT labeled as a green light
                    self.assertNotEqual(predicted_label, [0, 0, 1])
                except self.failureException as e:
                    # Print out an error message
                    print_fail()
                    print("Warning: A red light is classified as green.")
                    print('\n'+str(e))
                    return
        
        # No red lights are classified as green; test passed
        print_pass()
# <<
# ==================================================================================================================================
# END << CLASS << Tests
# ==================================================================================================================================



# <<
# ==================================================================================================================================
# END << SUBMODULE << traffic_light_classifier.__tests_subpkg__._tests_submod
# ==================================================================================================================================
