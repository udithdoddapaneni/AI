import subprocess as sb

a = 3
b = 4

p = sb.Popen("/home/udith/labs and projects/AI labs/connect4_l3_optimized/rough", stdout = sb.PIPE, stdin = sb.PIPE)
p.stdin.write(bytes(str(a)+"\n", 'utf-8'))
p.stdin.write(bytes(str(b)+"\n", 'utf-8'))
p.stdin.flush()
result = str(p.stdout.readline().strip())


print(result[2:len(result)-1])