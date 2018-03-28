Gid Post Results File 1.0 
### 
# MAT-fem Plate MZC v1.4 
# 
Result "Displacement" "Load Analysis"  1  Vector OnNodes 
ComponentNames "X-Displ", "Y-Displ", "Z-Displ" 
Values 
     1 0.0 0.0             0 
     2 0.0 0.0             0 
     3 0.0 0.0             0 
     4 0.0 0.0      -0.15625 
     5 0.0 0.0             0 
     6 0.0 0.0             0 
     7 0.0 0.0             0 
     8 0.0 0.0             0 
     9 0.0 0.0             0 
End Values 
# 
Result "Rotation" "Load Analysis"  1  Vector OnNodes 
ComponentNames "X-Rot", "Y-Rot", "Z-Rot" 
Values 
     1             0             0 0.0 
     2             0             0 0.0 
     3             0             0 0.0 
     4             0             0 0.0 
     5             0             0 0.0 
     6             0             0 0.0 
     7             0             0 0.0 
     8             0             0 0.0 
     9             0             0 0.0 
End Values 
# 
Result "Reaction" "Load Analysis"  1  Vector OnNodes 
ComponentNames "Z-Force", "X-Moment", "Y-Moment" 
Values 
     1           7.5      8.333333     -8.333333 
     2          17.5             0     -22.91667 
     3          17.5      22.91667             0 
     4             0             0             0 
     5           7.5      8.333333      8.333333 
     6           7.5     -8.333333     -8.333333 
     7          17.5  2.775558e-16      22.91667 
     8          17.5     -22.91667             0 
     9           7.5     -8.333333      8.333333 
End Values 
# 
Result "Moment" "Load Analysis"  1  Vector OnNodes 
ComponentNames "Mx", "My", "Mxy" 
Values 
     1 -2.220446e-16 -2.220446e-16       -0.4375 
     2         1.125          3.75             0 
     3          3.75         1.125             0 
     4        -4.875        -4.875             0 
     5 -2.220446e-16 -2.220446e-16        0.4375 
     6 -2.220446e-16 -2.220446e-16        0.4375 
     7         1.125          3.75             0 
     8          3.75         1.125             0 
     9 -2.220446e-16 -2.220446e-16       -0.4375 
End Values 
