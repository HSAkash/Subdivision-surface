import numpy as np
import trimesh


def center_point(p1, p2):
    """ 
    returns a point in the center of the 
    segment ended by points p1 and p2
    """
    return (p1+p2)/2

def sum_point(p1, p2):
    """ 
    adds points p1 and p2
    """
    return p1+p2

def div_point(p, d):
    """ 
    divide point p by d
    """
    return p/d

def mul_point(p, m):
    """ 
    multiply point p by m
    """ 
    return p*m

def get_face_points(input_points, input_faces):
    """
    From http://rosettacode.org/wiki/Catmull%E2%80%93Clark_subdivision_surface
    
    1. for each face, a face point is created which is the average of all the points of the face.
    """

    # 3 dimensional space
    
    NUM_DIMENSIONS = 3
    face_points = []
    for curr_face in input_faces:
        face_point = np.array([0.0, 0.0, 0.0])
        for curr_point_index in curr_face:
            curr_point = input_points[curr_point_index]
            # add curr_point to face_point
            # will divide later
            face_point += curr_point
        # divide by number of points for average
        num_points = len(curr_face)
        face_point /= num_points
        face_points.append(face_point)
        
    return np.array(face_points)


def get_edges_faces(input_points, input_faces):
    """
    
    Get list of edges and the one or two adjacent faces in a list.
    also get center point of edge
    
    Each edge would be [pointnum_1, pointnum_2, facenum_1, facenum_2, center]
    
    """
    
    # will have [pointnum_1, pointnum_2, facenum]
    
    edges = []
    
    # get edges from each face
    
    for facenum in range(len(input_faces)):
        face = input_faces[facenum]
        num_points = len(face)
        # loop over index into face
        for pointindex in range(num_points):
            # if not last point then edge is curr point and next point
            if pointindex < num_points - 1:
                pointnum_1 = face[pointindex]
                pointnum_2 = face[pointindex+1]
            else:
                # for last point edge is curr point and first point
                pointnum_1 = face[pointindex]
                pointnum_2 = face[0]
            # order points in edge by lowest point number
            if pointnum_1 > pointnum_2:
                temp = pointnum_1
                pointnum_1 = pointnum_2
                pointnum_2 = temp
            edges.append([pointnum_1, pointnum_2, facenum])





    
            
    # sort edges by pointnum_1, pointnum_2, facenum
    
    edges = sorted(edges)
    
    # merge edges with 2 adjacent faces
    # [pointnum_1, pointnum_2, facenum_1, facenum_2] or
    # [pointnum_1, pointnum_2, facenum_1, None]
    
    num_edges = len(edges)
    eindex = 0
    merged_edges = []
    
    while eindex < num_edges:
        e1 = edges[eindex]
        # check if not last edge
        if eindex < num_edges - 1:
            e2 = edges[eindex+1]
            if e1[0] == e2[0] and e1[1] == e2[1]:
                merged_edges.append([e1[0],e1[1],e1[2],e2[2]])
                eindex += 2
            else:
                merged_edges.append([e1[0],e1[1],e1[2],None])
                eindex += 1
        else:
            merged_edges.append([e1[0],e1[1],e1[2],None])
            eindex += 1
            
    # add edge centers
    
    edges_centers = []
    
    for me in merged_edges:
        p1 = input_points[me[0]]
        p2 = input_points[me[1]]
        cp = center_point(p1, p2)
        edges_centers.append(me+[cp])
            
    return np.array(edges_centers)


def get_edge_points(input_points, edges_faces, face_points):
    """
    for each edge, an edge point is created which is the average 
    between the center of the edge and the center of the segment made
    with the face points of the two adjacent faces.
    """
    
    edge_points = []
    
    for edge in edges_faces:
        # get center of edge
        cp = edge[4]
        # get center of two facepoints
        fp1 = face_points[edge[2]]
        # if not two faces just use one facepoint
        # should not happen for solid like a cube
        if edge[3] == None:
            fp2 = fp1
        else:
            fp2 = face_points[edge[3]]
        cfp = center_point(fp1, fp2)
        # get average between center of edge and
        # center of facepoints
        edge_point = center_point(cp, cfp)
        edge_points.append(edge_point)      
        
    return np.array(edge_points)


def get_avg_face_points(input_points, input_faces, face_points):
    """
    
    for each point calculate
    
    the average of the face points of the faces the point belongs to (avg_face_points)
    
    create a list of lists of two numbers [facepoint_sum, num_points] by going through the
    points in all the faces.
    
    then create the avg_face_points list of point by dividing point_sum (x, y, z) by num_points
    
    """
    
    # initialize list with [[0.0, 0.0, 0.0], 0]
    
    num_points = len(input_points)
    
    temp_points = []
    
    for pointnum in range(num_points):
        temp_points.append([[0.0, 0.0, 0.0], 0])
        
    # loop through faces updating temp_points
    
    for facenum in range(len(input_faces)):
        fp = face_points[facenum]
        for pointnum in input_faces[facenum]:
            tp = temp_points[pointnum][0]
            temp_points[pointnum][0] = sum_point(tp,fp)
            temp_points[pointnum][1] += 1
            
    # divide to create avg_face_points
    
    avg_face_points = []
    
    for tp in temp_points:
       afp = div_point(tp[0], tp[1])
       avg_face_points.append(afp)
       
    return np.array(avg_face_points)



input_points = [
 [ 0.69999999, -0.475077  , -0.69999999],
 [-0.69999999, -0.475077  ,-0.69999999],
 [-0.69999999 ,-0.475077  ,  0.69999999],
 [ 0.69999999 ,-0.475077  ,  0.69999999],
 [ 1.  ,       -0.69999999 ,-1.        ],
 [-1.   ,      -0.69999999 ,-1.        ],
 [-1.   ,      -0.69999999 , 1.        ],
 [ 1.     ,    -0.69999999  ,1.        ],
 [ 0.5   ,      0.0287423  ,-1.        ],
 [-0.5    ,     0.0287423  ,-1.        ],
 [-1.    ,      0.0287423 , -0.5       ],
 [-1.     ,     0.0287423  , 0.5       ],
 [-0.5     ,    0.0287423  , 1.        ],
 [ 0.5   ,      0.0287423  , 1.        ],
 [ 1.     ,     0.0287423 ,  0.5       ],
 [ 1.     ,     0.0287423 , -0.5       ],
 [ 1.25401998 , 1.09021997 ,-1.25401998],
 [-1.25401998  ,1.09021997 ,-1.25401998],
 [-1.25401998 , 1.09021997 , 1.25401998],
 [ 1.25401998  ,1.09021997 , 1.25401998],
 [ 0.671875  ,  4.    ,     -0.671875  ],
 [-0.671875  ,  4.      ,   -0.671875  ],
 [-0.671875   , 4.     ,     0.671875  ],
 [ 0.671875   , 4.     ,     0.671875  ]]

input_faces= [
 [ 0  ,1  ,2  ,3],
 [ 4 ,5 , 1 , 0],
 [ 5 , 6 , 2 , 1],
 [ 6 , 7 , 3 , 2],
 [ 7 , 4 , 0 , 3],
 [ 8 , 9 , 5  ,4],
 [10 ,11 , 6 , 5],
 [12 ,13 , 7 , 6],
 [14, 15 , 4  ,7],
 [ 9 ,17 ,10 , 5],
 [11, 18 ,12 , 6],
 [13 ,19 ,14 , 7],
 [15 ,16  ,8 , 4],
 [16 ,17 , 9 , 8],
 [17 ,18 ,11 ,10],
 [18 ,19 ,13, 12],
 [19 ,16, 15 ,14],
 [20 ,21 ,17, 16],
 [21 ,22 ,18 ,17],
 [22 ,23 ,19, 18],
 [23 ,20 ,16, 19]]

input_points = np.array(input_points)
input_faces = np.array(input_faces)
face_points = get_face_points(input_points, input_faces)
print(face_points)

# face_points = (21, 3)

















# p1=np.array([ 0.69999999, -0.475077 ,  -0.69999999],)
# p2= np.array([-0.69999999 ,-0.475077  , -0.69999999],)
# # cp: [0.0, -0.4750770032405853, -0.699999988079071],
# # cp = center_point(p1, p2)
# sp = sum_point(p1, p2)
# print("p1:", p1)
# print("p2:", p2)
# # print("cp:", cp)
# print("sp:", sp)