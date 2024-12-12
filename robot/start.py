import win32com.client
import numpy

robapp = win32com.client.Dispatch('Robot.Application')
params = win32com.client.Dispatch("Robot.FeResultParams")
red = win32com.client.Dispatch("Robot.FeResultReduced")

def res(bar_no,loadcase_no,ratio):
    return robapp.Project.Structure.Results.Bars.Forces.Value(bar_no,loadcase_no,ratio).MY/1000

def length(bar_no):
    return robapp.Project.Structure.Bars.Get(bar_no).Length

def ratio(face_thk,length,d_eff=0):
    return (face_thk+d_eff)/length

def max_res(bar_no,loadcase_no,inc):
    result = [res(bar_no,loadcase_no,i) for i in numpy.arange(0,1+inc,inc)]
    return max(result)

# length=length(1)
# r = ratio(0.5,length,d_eff=0.4)
# print(res(1,1,r))
# print(max_res(1,1,0.005))

def get_finite_element_results(panel_num, node_num, case_num):
    """
    Retrieve finite element results from the Robot API for a specific panel, node, and load case.

    Args:
        panel_num (int): Panel number.
        node_num (int): Node number.
        case_num (int): Case number.

    Returns:
        dict: Dictionary containing the finite element result values (MXX, MYY, MXY).
    """

    # Create a new instance of RobotFeResultParams
    params = win32com.client.Dispatch("Robot.FeResultParams")

    # Set the panel, node, and case numbers
    params.Panel = panel_num
    params.Node = node_num
    params.Case = case_num

    # Select the layer
    I_FLT_MIDDLE = 1  # Example value for the middle layer
    params.Layer = I_FLT_MIDDLE

    # Retrieve detailed finite element results
    detFE = robapp.Project.Structure.Results.FiniteElems.Reduced(params)

    # Extract required result values
    results = {
        "MXX": detFE.MXX/1000,
        "MYY": detFE.MYY/1000,
        "MXY": detFE.MXY/1000
    }

    return results


# # Example usage
# panel_num = 6
# node_num = 18
# case_num = 1

# try:
#     fe_results = get_finite_element_results(panel_num, node_num, case_num)
#     print("Finite Element Results:", fe_results)
# except Exception as e:
#     print("Error:", e)

print(dir(params))
# print(robapp.Project.Structure.Results.Bars.Deflections.Value(1,1,0).UZ)
# print(dir(robapp.Project.Structure.GroupObjects.GetContents))
# select = win32com.client.Dispatch('Robot.Selection')
# print(dir(select.Get))

def listno_generator(input_string):
    result = []
    # Split the string into parts
    parts = input_string.split()
    
    for part in parts:
        # Check if the part is a range (e.g., '1to6')
        if 'to' in part:
            start, end = map(int, part.split('to'))
            result.extend(range(start, end + 1))  # Expand the range and add to the result
        else:
            result.append(int(part))  # Add individual numbers
            
    return result


# print(listno_generator("75to82 93 160 173 174 201"))
# print(dir(params))

# b = RobApp.Project.Structure.Bars
# b_start = b.Get(1).Number
# print(b_start)
# print(dir(b))
# a = RobApp.Project.Structure.Results.Bars.Forces.MaxValue(1,1).MY/1000