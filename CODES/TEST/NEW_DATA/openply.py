import open3d as o3d

#Zita Kitti
#pcd = o3d.io.read_point_cloud("/Volumes/TIMKA/NEW_CNN/NewData/ZitaKitti/0000.ply")

#Velodyne
pcd = o3d.io.read_point_cloud("/Volumes/TIMKA/NEW_CNN/NewData/Velodyne/0000000000.ply")

#Sick
#pcd = o3d.io.read_point_cloud("/Volumes/TIMKA/NEW_CNN/NewData/Sick/0000000000.ply")
# Print the point cloud
print(pcd)

# Visualize the point cloud
o3d.visualization.draw_geometries([pcd])