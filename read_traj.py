#pip install numpy cython mdtraj

import mdtraj as md

dcd_files = "/Users/dubc/ubq_wb_eq.dcd"
pdb_files = "/Users/dubc/ubq_wb.pdb"
main_files = "/Users/dubc/main_chain.dat"
side_files = "/Users/dubc/side_chain.dat"

traj = md.load(dcd_files, top=pdb_files)

phi = md.compute_phi(traj)
psi = md.compute_psi(traj)
angle_mount = len(phi[0])
frame = len(phi[1])

files = open(main_files, 'w')
char = ''
for frame_cur in range(0, frame):
    for index in range(0, angle_mount):
        phi_cur = phi[1][frame_cur][index]
        psi_cur = psi[1][frame_cur][index]
        char = '%10.6lf %10.6lf %s'%(phi_cur, psi_cur, char)
    char = '%s \n'%(char)
    files.write(char)
    char = ''
files.close()

files = open(side_files, 'w')
chi1 = md.compute_chi1(traj)
chi2 = md.compute_chi2(traj)
chi3 = md.compute_chi3(traj)
chi4 = md.compute_chi4(traj)
for frame_cur in range(0, frame):
    for index in range(0, len(chi1[0])):
        chi_cur = chi1[1][frame_cur][index]
        char = '%10.6lf %s'%(chi_cur, char)
    for index in range(0, len(chi2[0])):
        chi_cur = chi2[1][frame_cur][index]
        char = '%10.6lf %s'%(chi_cur, char)
    for index in range(0, len(chi3[0])):
        chi_cur = chi3[1][frame_cur][index]
        char = '%10.6lf %s'%(chi_cur, char)
    for index in range(0, len(chi4[0])):
        chi_cur = chi4[1][frame_cur][index]
        char = '%10.6lf %s'%(chi_cur, char)
    char = '%s \n'%(char)
    files.write(char)
    char = ''
files.close()
