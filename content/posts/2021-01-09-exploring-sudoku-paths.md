---
title: Exploring paths for Sudoku variants with Python
layout: post
include_syntax_styles: true
notes: |
    Created with https://swaroopg92.github.io/penpa-edit/ -- create puzzle, use
    Firefox's screenshot function (the export function does some dithering that)
    messes with compression, and then use squoosh to compress PNGs. Results in
    1-2KB images, rather than 25-30KB each.
    npx @squoosh/cli --quant '{"enabled":true,"zx":0,"maxNumColors":6,"dither":1}' --oxipng '{"level":3}' *.png
    base64 <snake.png | wl-copy
---
<style>.content img { max-width: 380px; }</style>
One of my college friends has an interest in Sudoku variants. Generally, that
manifests in the two of us solving puzzles curated by
[Cracking the Cryptic](https://www.youtube.com/channel/UCC-UOdK8-mIjxBQm_ot1T-Q),
but occasionally it ends up with me trying to solve a puzzle he's created.
A while back, he and I were chatting about one of his ideas for the basis of
a puzzle. It's based around a snake in the grid (for an example of another
puzzle using a snake, check out
[this puzzle by CtC](https://www.youtube.com/watch?v=IDp1EjkerR0)). His puzzle
requires that its snake alternates successive even digits and odd digits, is
unambiguous, and visits at least one cell in every box (as well as, of course,
being a valid sudoku puzzle!).

Let's talk about those rules in a bit more depth:

 * **Snake**: A snake is a one-wide orthogonally connected path. Much like in
   the classic Snake game, it can't touch itself anywhere along its length
   (although diagonal adjacency is fine). The one in this puzzle has alternating
   even and odd digits along its length, represented in this post by red and
   blue respectively:
![a snake matching the above description](data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAXwAAAF8CAMAAAD7OfD4AAAASFBMVEX////A4P//o6NfikVeiURA
k0xZiEFYiEE2jkBEhTVDhTQhgCEggCAfgB8dHR0cHBwbGxsQEBAODxAQDQ0MDhAQCgoJCQkAAAC7
9TkfAAAEmElEQVR42u3d225URxAF0Jpb7GCkZCIc/v/zIIJICGPAc0G8mrZUWOd4+nSt/dyqbS8d
9cuo1KuQi2UV0gj84QO/GfjDB34z8IcP/GbgDx/4zcAfPvCbgT984DcDf/jAbwb+8IHfDPzh08D/
6zpkhtx/SuC/DZkl7+C30hX+u8So/f/xvFMa4cOv3Qgffs1G+PBrNsKHX7MRPvyajfDh12yED79m
I3z4NRvhw6/ZCB9+zUb48Gs2wodfsxE+/JqN8OHXbIQPv2YjfPg1G+HDr9kIvzv874lpf5wikfUx
cWgTcZpqVmxSoyKOU82KdYpr0i//9kMk8k/m1L8R/001K95kTt1GvJ9qVuwzp97Chw8fPnz48OHD
hw8fPnz48OHDhw8fPnz48Mvjr6/jebmJuIspMn/j6nz62iX+qxgfPyK+dIm/267gu/Pnu/NfwYcP
Hz58+PDhw4cPHz58+PDhw4cPHz58+PDhJ7cRD5HI9iFxaBdxmGpW7FKjIlJ/2DEe5WvEdTzKJsVl
D7fZmP/y278/7j9agoYPHz58+PDhw4cPfzmN8OHDhw8fPnz48OHDhw9/VvzX59Vn+L58+PDhw4cP
Hz58+PDhw4cPH/4SGuHDhw8fPnz48OFPjS8zBP4TgT983Pm/1Xjb6wY6fPjw4cOHDx8+fPjw4cOH
D38pjfDhw4cPHz78i+DfnFd38H358OHDhw8fPnz48OHDhw8fPvwlNMKHDx8+fPjw4cOHPxJ+6rG/
YySyOSUOrSOOU82KdWpUROoP6/VtxDcdvNE5+zukvW6gw4cPHz58+PDhw4cPHz58+PDhw4cPHz58
+PCXiH+1XZ0jk8R/lM8LN/aKfxMR8OHP2Pjt0Cv+3eh3/s/Ahw8fPnz48OHDhw8fPnz48OHDhw8f
Pnz48Mvjp9brTvEo9xF/xqOsD4lR24iHxLHdITLDUqMiDlPNit2ztxF73VHtYg93ykb4fTXChw8f
Pnz48OHDhw8fPnz48OHDhw8fPnz4Wfxe3w2E78uHDx8+fPjw4cOHDx8+fPhLaYQPHz58+PDhw4cP
H34VfJk+8J8I/OHz4kvQ+4+LuYF7ufPhw4cPHz58+PDhw4cPHz58+PDhL6ERPnz48BeM//q8+gzf
l7+MRvjw4cOHDx8+fPjw4cOHDx8+fPjw4cOHDx9+/43w4cOf5W3EY2LUJuKUOJaaFZvUqIjjVLNi
3evbiPO/0Xn5d0j3HzrdQIcPHz58+PDhw4cPHz58+PDhw4cPHz58+PDhd4efS+L3x2Qu0Pj9AP9i
+Of7LvGvNhXw789d4v+MOx8+fPjw4cOHDx8+fPjw4cOHDx8+fPjw4cOHXwA/tV53iES2D4lDu4jD
VLNilxoV8TDVrNg+exux1x3VCo3w4ddshA+/ZiN8+DUb4cOv2Qgffs1G+PBrNsKHX7MRPvyajfDh
12yED79mI3z4NRvhw6/ZCB9+zUb48Gs2wodfsxE+/JqN8OHXbITfHb5MH/hPpB/8v69CZsj5/a/4
8mKB31HgNwN/+MBvBv7wgd8M/OEDvxn4wwd+M/CHD/xm4A8f+M3AHz4/AB0L2kBP++2sAAAAAElF
TkSuQmCC)
 * **visits a cell in every box**: The above snake fills this requirement as
   well. The following (shorter) snake does, too:
![a shorter snake which also visits each box](data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAXwAAAF8CAMAAAD7OfD4AAAATlBMVEX////A4P//o6NPnGFMml5K
mVtIl1hAk0w5kEQ5j0NEhTVAhTIigSMhgCEggCAfgB8dHR0cHBwbGxsQEBAODxAQDQ0MDhAQCgoJ
CQkAAAD0Q4fDAAAEaklEQVR42u3d0U4USxiF0X9EHD3CSc7RiL7/w6lBE6MYEIXxxhucIl0hPdpd
e+1rUh+sdJqrSm/K/to2ZY3BH37wm4M//OA3B3/4wW8O/vCD3xz84Qe/OfjDD35z8Icf/ObgDz/4
zcEffg38/56WHWCXnzrw35QdZG/ht7Yo/Lc1vRcf62E/pQgffnYRPvzMInz4mUX48DOL8OFnFuHD
zyzCh59ZhA8/swgffmYRPvzMInz4mUX48DOL8OFnFuHDzyzCh59ZhA8/swgffmYR/uLwr2t6T65r
rp96klH05C+pCB9+ZhE+/MwifPiZRfjwM4vw4WcW4cPPLMKHn1mEDz+zCB9+ZhE+/MwifPiZRfjw
M4vw4WcW4cPPLMKHn1mEDz+zCB9+ZhE+/MziwW8j3tT0jqpua3qPbqrnsK6jqrp+sXXfRnx1XtN7
XfW+pvfyfLbiWdW7nr/xw6pfO/Dhw4cPHz58+PDhw4cPHz58+PDhw4cPHz78NeIf/VO/73nV1zrk
eoqb3fer4fFPa5n4VfVlePzj7Qa+d/7dncKHDx8+fPjw4cOHDx8+fPjw4cOHDx8+fPgrw7f5B/+e
wR9+LkH/Ku7/lzmputg763zV/3Dhw4cPHz58+PDhw4cPHz58+PDhw4cPHz784fBPd5sv8D358OHD
hw8fPnz48OHDhw8fPnz48OHDhw8fPnz48OEvEX/GbyN2HfU3ijd1d1dVTwf7NuJyn/zFXoKGDx8+
fPjw4cOHDx8+fPjw4cOHDx8+fPjw4cNfIv6/u81n+J58+PDhw4cPHz58+PDhw4cPHz58+PDhw4cP
Hz58+PCXiD/j3cDbmt6jqpua3tFt9RzWeTfw98Muq57tnbXu24hnvR9Inetjq/XifOX3cOHDhw8f
Pnz48OHDhw8fPnz48OHDhw8fPnz42fjPjja7urvnVV/rYftxtQ/m24j34p9U1Xz4deHJh78a/Iu5
3vkn8OHDhw8fPnz48OHDhw8fPnz48OHDhw8ffjC+zT/49wz+8Jv3nd/3np6+bPy6Uew+q/FT0ztb
8CVo+PDhw4cPHz58+PDhw4cPHz58+PDhw4cPfzz8nvXdAoMP/6D4j7eXt3Phb7e1mw//2/Xw+I11
4/cVH37nHT58+PDhw4cPHz58+PDhw4cPHz58+PDhw4cP/09/G/F7Te94sth/Vh3/qOk9rur6xdb9
bcTlfhW0r7jq186KKOBHFeHDzyzCh59ZhA8/swgffmYRPvzMInz4mUX48DOL8OFnFuHDzyzCh59Z
hA8/swgffmYRPvzMInz4mUX48DOL8OFnFuHDzywe/DZi11EZRU/+korw4WcW4cPPLMKHn1mEDz+z
CB9+ZhE+/MwifPiZRfjwM4vw4WcW4cPPLMKHn1mEDz+zCB9+ZhE+/MwifPiZRfjwM4vw4WcW4S8O
3+Yf/Hu2HPz/t2UH2O7dPr79scFf0OA3B3/4wW8O/vCD3xz84Qe/OfjDD35z8Icf/ObgDz/4zcEf
fj8BenbrQA4hsTMAAAAASUVORK5CYII=)
 * and the big constraint, **is unambiguous**: Given the pattern of even and odd
   digits in the grid, there is exactly one direction the snake could continue
   at any point and still satisfy the parity constraint. To see this happen, we
   also have to have some information about the parity of the cells surrounding
   the snake. In general, each cell of the snake is touching either one (if it's
   the head/tail) or two (if it's part of the body) other cells that are snake
   cells. These must be of the opposite parity. The other cells must be of the
   same parity.

   For example, suppose that the head of the snake is even, and continues into
   the (odd) cell to its right:
![sudokus form](data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAXwAAAF8CAMAAAD7OfD4AAAAOVBMVEX////A4P//o6NNm19JmFle
iURYiEEhgCEggCAdHR0cHBwbGxsQEBAODxAQDQ0MDhAQCgoJCQkAAAD2nVmLAAADuUlEQVR42u3d
22oUQQBF0R4To3gB9f+/MYIIgcnND7AGGumJRe11novesGj6rejTZv9tp80Gg7/84A8Hf/nBHw7+
8oM/HPzlB384+MsP/nDwlx/84eAvP/jDwV9+8IeDv/wG+J8+bnaFPTzswP+x2VV2D3+0qfDvdzzq
y+/t304pwoffLsKH3yzCh98swoffLMKH3yzCh98swoffLMKH3yzCh98swoffLMKH3yzCh98swoff
LMKH3yzCh98swoffLMKH3yzCnw7/vONpdy/bjr173nHoZmfxvB116u7ti4e++d9+bTv2dc+p71O8
h7O8+fDhw4cPHz58+PDhw4cPHz58+PDhw4cPHz78VfFvbrZde3qGfzj+3bZvr2f4h+Pfnk678B9f
4Pvmw4cPHz58+PDhw4cPHz58+PDhw4cPHz58+PDhX/E24tO2Y7ePOw69dxtxrreiUIQPv1mED79Z
hA+/WYQPv1mED79ZhA+/WYQPv1mED79ZhA+/WYQPv1mED79ZhA+/WYQPv1mED79ZhA+/WYQPv1mE
D79ZhD8dvh0/+BcGf/n55s9UhA+/WYQPv1mED79ZhA+/WYQPv1mED79ZhA+/WYQPv1mED79ZhA+/
WYQPv1mED79ZhA+/WYQPv1mED79ZhA+/WYQPv1mEPx1+4U+F/o3YLsKH3yzCh98swoffLMKH3yzC
h98swoffLMKH3yzCh98swoffLMKH3yzCh98swoffLMKH3yzCh98swoffLMKH3yzCh98swoffLLqN
6DZiswgffrMIH36zCB9+swgffrMIH36zCB9+swgffrMIH36zCB9+swgffrMIH36zCB9+swgffrMI
H36zCB9+swgffrMIH36zCH86fDt+8C8M/vLzzZ+pCB9+swgffrMIH36zCB9+swgffrMIH36zCB9+
swgffrMIH36zCB9+swgffrMIH36zCB9+swgffrMIH36zCB9+swgffrMIfzr8wp8K/RuxXYQPv1mE
D79ZhA+/WYQPv1mED79ZhA+/WYQPv1mED79ZhA+/WYQPv1mED79ZhA+/WYQPv1mED79ZhA+/WYQP
v1mED79ZhA+/WXQb0W3EZhE+/GYRPvxmET78ZhE+/GYRPvxmET78ZhE+/GYRPvxmET78ZhE+/GYR
PvxmET78ZhE+/GYRPvxmET78ZhE+/GYRPvxmEf50+Hb84F/YPPifP2x2hb3+/Bvf3mzwJxr84eAv
P/jDwV9+8IeDv/zgDwd/+cEfDv7ygz8c/OUHfzj4y+8PfCAVQIawBZcAAAAASUVORK5CYII=)

   To ensure there's no ambiguity that the snake continues to the right, all of
   the other cells must be invalid for the snake to enter; that is, they must
   all have the same parity as the head:
![a puzzle fine](data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAXwAAAF8CAMAAAD7OfD4AAAAOVBMVEX////A4P//o6NNm19JmFle
iURYiEEhgCEggCAdHR0cHBwbGxsQEBAODxAQDQ0MDhAQCgoJCQkAAAD2nVmLAAADxElEQVR42u3d
3UoQQQCG4TXNoiyq+79GiwgEf7sARxhCbZz3+Y6HfeFh2bNhTw77bzs5bDD42w/+cPC3H/zh4G8/
+MPB337wh4O//eAPB3/7wR8O/vaDPxz87Qd/OPjbb4D/6eNhL7Crqwn8H4e9yC7hj7YU/uXEo779
ngleTJyaLV78OaZOvZkifPjw4cOHDx8+fPjw4cOHDx8+fPjw4cOHD3/9Inz48OHDhw8fPnz48OHD
hw8fPnz48OHDhw9//SJ8+PDhL4F/P/G0d/fHzKm7iUOnx3E9cex84tDkqfPXL07j/5p42tepN//L
zKnvS7yHq7z58OHDhw8fPnz48OHDhw8fPnz48OHDhw8fPvxd8U9Pj6nd3sF/dvzzY24P1/CfHf/s
5GQK/+Yevm8+fPjw4cOHDx8+fPjw4cOHDx8+fPjw4cOHDx/+v+HfTjztbO424s3EofduI7qHu8ab
Dx8+fPjw4cOHDx8+fPjw4cOHD/8tFOHDhw8fPnz48OHDhw8fPnz48OHDhw8fPnz46xfhw4cPHz58
+PDhw39NfHuBwX9i8LffY/xVv4eFInz4zSJ8+M0ifPjNInz4zSJ8+M0ifPjNInz4zSJ8+M0ifPjN
Inz4zSJ8+M0ifPjNInz4zSJ8+M0ifPjNInz4zSJ8+M0i/OXwC38qfNP/RtzuPVzlzU9SwE8V4cNv
FuHDbxbhw28W4cNvFuHDbxbhw28W4cNvFuHDbxbhw28W4cNvFuHDbxbhw28W4cNvFuHDbxbhw28W
4cNvFuHDbxbdRnQbsVmED79ZhA+/WYQPv1mED79ZhA+/WYQPv1mED79ZhA+/WYQPv1mED79ZhA+/
WYQPv1mED79ZhA+/WYQPv1mED79ZhA+/WYS/HL49/+A/Mfjbzzd/pSJ8+M0ifPjNInz4zSJ8+M0i
fPjNInz4zSJ8+M0ifPjNInz4zSJ8+M0ifPjNInz4zSJ8+M0ifPjNInz4zSJ8+M0ifPjNIvzl8At/
KvRvxHYRPvxmET78ZhE+/GYRPvxmET78ZhE+/GYRPvxmET78ZhE+/GYRPvxmET78ZhE+/GYRPvxm
ET78ZhE+/GYRPvxmET78ZhE+/GbRbUS3EZtF+PCbRfjwm0X48JtF+PCbRfjwm0X48JtF+PCbRfjw
m0X48JtF+PCbRfjwm0X48JtF+PCbRfjwm0X48JtF+PCbRfjwm0X4y+Hb8w/+E1sH//OHw15gDz8f
49urDf5Cgz8c/O0Hfzj42w/+cPC3H/zh4G8/+MPB337wh4O//eAPB3/7/QWeKhVAjuAPNgAAAABJ
RU5ErkJggg==)

   Now, each box must contain a 1 through 9; that is, four even and five odd
   digits. This one already contains all four even digits, so the unfilled cells
   must be odd:
![yet you'll need only](data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAXwAAAF8CAMAAAD7OfD4AAAAM1BMVEX////A4P//o6NNm19JmFle
iURYiEEhgCEggCAdHR0cHBwbGxsQEBAMDhAQCgoJCQkAAADPLnw0AAADsElEQVR42u3dTU4VQQBG
0UKQgWhk/6sUY2JUflwARSjMA5u65xtXcl/O6/Ss0mfD/tvOhk0Gf/vBnw7+9oM/HfztB386+NsP
/nTwtx/86eBvP/jTwd9+8KeDv/3gTwd/+03wP10Oe4X9+rmAfz3sVfYN/myHwr8Zz+/Lj5Xg1cqp
r5MfNtnnpeLSqetDFOHDhw8fPnz48OHDhw8fPnz48OHDhw8fPnz48OHDhw8fPnz48OHDhw8fPnz4
8OHDhw8fPnz48OHDh78J/v14fh/ux8qpu4VD52PcLhy7uB2nOnXx9sVl/O8r/7cn/0VF+PDhw4cP
Hz58+PDhw4cPHz58+PDhw4cPH34e//x8LO32Dv7J8S/H2h5+wz85/sXZ2VjZn3v43vnw4cOHDx8+
fPjw4cOHDx8+fPjw4cOHDx8+fPj/hr90hdBtxBcV3cN9D08+fPjw4cOHDx8+fPjw4cOHDx8+fPjw
4cOHDx8+fPjw4cOHDx8+fPjw4cOHDx8+fPjw4cOHDx8+fPjw3x2+nX7wnxj87fcY/6jvw0IRPvxm
ET78ZhE+/GYRPvxmET78ZhE+/GYRPvxmET78ZhE+/GYRPvxmET78ZhE+/GYRPvxmET78ZhE+/GYR
PvxmET78ZhH+4fALXyo87LcRk8/hUZ78JAX8VBE+/GYRPvxmET78ZhE+/GYRPvxmET78ZhE+/GYR
PvxmET78ZhE+/GYRPvxmET78ZhE+/GYRPvxmET78ZhE+/GYRPvxm0W1EtxGbRfjwm0X48JtF+PCb
Rfjwm0X48JtF+PCbRfjwm0X48JtF+PCbRfjwm0X48JtF+PCbRfjwm0X48JtF+PCbRfjwm0X48JtF
+IfDt9MP/hODv/28849UhA+/WYQPv1mED79ZhA+/WYQPv1mED79ZhA+/WYQPv1mED79ZhA+/WYQP
v1mED79ZhA+/WYQPv1mED79ZhA+/WYQPv1mEfzj8wpcKfRuxXYQPv1mED79ZhA+/WYQPv1mED79Z
hA+/WYQPv1mED79ZhA+/WYQPv1mED79ZhA+/WYQPv1mED79ZhA+/WYQPv1mED79ZhA+/WXQb0W3E
ZhE+/GYRPvxmET78ZhE+/GYRPvxmET78ZhE+/GYRPvxmET78ZhE+/GYRPvxmET78ZhE+/GYRPvxm
ET78ZhE+/GYRPvxmEf7h8O30g//EjoN/9XHYK+zh5jG+vdngH2jwp4O//eBPB3/7wZ8O/vaDPx38
7Qd/OvjbD/508Lcf/Ongb7+/b+oVQPd5r/gAAAAASUVORK5CYII=)

   The only place the snake can proceed, then, is directly into the second box:
![a one](data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAXwAAAF8CAMAAAD7OfD4AAAANlBMVEX////A4P//o6NfikVeiURZ
iEFYiEEhgCEggCAdHR0cHBwbGxsQEBAQDQ0MDhAQCgoJCQkAAACNR84eAAADyUlEQVR42u3dUUtU
QQCG4dGsKC3y///IDAMDM7vXkT3Gbp3mfb7rgXd5OOzdMGfD/tnOhk0Gf/nBnw7+8oM/HfzlB386
+MsP/nTwlx/86eAvP/jTwV9+8KeDv/zgTwd/+U3wP74fdoL9uNuAfz3sJPsKf7Zd4d+Mw/t8uyV4
teXUl8kPm+zq+zjWqetdFOHDhw8fPnz48OHDhw8fPnz48OHDhw8fPnz48OHDhw8fPnz48OHDhw8f
Pnz48OHDhw8fPnz48OHDh78I/q9xeOdbDo3zh3F4bzYW77cU395vOTTGpmNHLG7G/zYO79MRv/xt
xcvbxJcPHz58+PDhw4cPHz58+PDhw4cPHz58+PDhw18V//xi/Nk+jHE3nu7hAf4r8N+NY+I/3sN/
Bf7F2dkR8e8f4fvPhw8fPnz48OHDhw8fPnz48OHDhw8fPnz48OHDf3ps0xXCo95G/DkO76JxG9E9
XJeg4cOHDx8+fPjw4cOHDx8+fPjw4cOHDx8+fPjw4cOHDx8+fPjw4cOHDx8+fPjw4cOHDx8+fPjw
4cOHvxnfTjD4Lwz+8nuOv9f/w0IRPvxmET78ZhE+/GYRPvxmET78ZhE+/GYRPvxmET78ZhE+/GYR
PvxmET78ZhE+/GYRPvxmET78ZhE+/GYRPvxmET78ZhH+7vA3Pfb3n79UuNu3EZPf4V6+/CQF/FQR
PvxmET78ZhE+/GYRPvxmET78ZhE+/GYRPvxmET78ZhE+/GYRPvxmET78ZhE+/GYRPvxmET78ZhE+
/GYRPvxmET78ZtFtRLcRm0X48JtF+PCbRfjwm0X48JtF+PCbRfjwm0X48JtF+PCbRfjwm0X48JtF
+PCbRfjwm0X48JtF+PCbRfjwm0X48JtF+PCbRfi7w7fjD/4Lg7/8/OfvqQgffrMIH36zCB9+swgf
frMIH36zCB9+swgffrMIH36zCB9+swgffrMIH36zCB9+swgffrMIH36zCB9+swgffrMIH36zCH93
+IWXCr2N2C7Ch98swoffLMKH3yzCh98swoffLMKH3yzCh98swoffLMKH3yzCh98swoffLMKH3yzC
h98swoffLMKH3yzCh98swoffLMKH3yy6jeg2YrMIH36zCB9+swgffrMIH36zCB9+swgffrMIH36z
CB9+swgffrMIH36zCB9+swgffrMIH36zCB9+swgffrMIH36zCB9+swh/d/h2/MF/YfvBv3w37AR7
vHmOb39t8Hc0+NPBX37wp4O//OBPB3/5wZ8O/vKDPx385Qd/OvjLD/508Jffb7s4FUBB5F03AAAA
AElFTkSuQmCC)

   If we continue to the right, we would need at least five red cells in the top
   middle box (try it out, if you like!) so now we have to move down...
![through nine](data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAXwAAAF8CAMAAAD7OfD4AAAAQlBMVEX////A4P//o6NPnGFKmVte
iURYiEFDhTQigSMhgCEggCAfgB8dHR0cHBwbGxsQEBAODxAQDQ0MDhAQCgoJCQkAAABkBAFnAAAD
+ElEQVR42u3dzWpUWRhG4Z2uxE7TdPuD3v8FGlFBUYxRR07MjjlKlTns9bzjj6zwUNQkbHI27MF2
Nmwy+MsP/nTwlx/86eAvP/jTwV9+8KeDv/zgTwd/+cGfDv7ygz8d/OUHfzr4y2+C/9/lsBPsw7sN
+C+GnWQv4c+2K/yrcf+evd4SfLLl6vkYrzacPd5UfPx2w9GLCcX0Zx2vCB8+fPjw4cOHDx8+fPjw
4cOHDx8+fPjw4cOHDx8+fPjw4cOHDx8+fPjw4cOHDx8+fPjw4cOHDx8+/HXxv4z799fkaHJ1s+Ho
8BDFTWc341hXh4342z6HT0/6yT998epoxaebivDhw4cPHz58+PDhw4cPHz58+PDhw4cPHz78PP7h
Yvze/h3j/Y+/19eba/i/kLwcR8H/vo/wfyF5fjiDv8J3/iV8+PDhw4cPHz58+PDhw4cPHz58+PDh
w4cPH/5+8Tc9rzvp28CPk79KHj5vKZ5fbzi6GGPT2fU41tXFjt/h/lj8Z4wPt967vkm8w4UPHz58
+PDhw4cPHz58+PDhw4cPHz58+PDhw4cPH/4c/3B+/QX+A+B/H3z48OHDhw8fPnz48OHDhw8fPnz4
8OHDhw//J/h2gsG/Y/CX3238vX4fForw4TeL8OE3i/DhN4vw4TeL8OE3i/DhN4vw4TeL8OE3i/Dh
N4vw4TeL8OE3i/DhN4vw4TeL8OE3i/DhN4vw4TeL8OE3i/B3h/9p3L9Hn8axrh41ij75eyrCh98s
woffLMKH3yzCh98swoffLMKH3yzCh98swoffLMKH3yzCh98swoffLMKH3yzCh98swoffLMKH3yzC
h98swoffLMKH3yx6jeg1YrMIH36zCB9+swgffrMIH36zCB9+swgffrMIH36zCB9+swgffrMIH36z
CB9+swgffrMIH36zCB9+swgffrMIH36zCB9+swh/d/h2/MG/Y/CXn+/8PRXhw28W4cNvFuHDbxbh
w28W4cNvFuHDbxbhw28W4cNvFuHDbxbhw28W4cNvFuHDbxbhw28W4cNvFuHDbxbhw28W4cNvFuHv
Dr/wnwr9b8R2ET78ZhE+/GYRPvxmET78ZhE+/GYRPvxmET78ZhE+/GYRPvxmET78ZhE+/GYRPvxm
ET78ZhE+/GYRPvxmET78ZhE+/GYRPvxm0WtErxGbRfjwm0X48JtF+PCbRfjwm0X48JtF+PCbRfjw
m0X48JtF+PCbRfjwm0X48JtF+PCbRfjwm0X48JtF+PCbRfjwm0X48JtF+LvDt+MP/h3bD/7/fw87
wb5e3ca3Pzb4Oxr86eAvP/jTwV9+8KeDv/zgTwd/+cGfDv7ygz8d/OUHfzr4y+8b7EA7QE48e9MA
AAAASUVORK5CYII=)

   Repeating this logic eventually gets us here. This scenario, however, is already
   broken---there simply isn't a way to get the snake back into the top right box,
   if we can't put a red cell in that middle row.
![Burma-Shave](data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAXwAAAF8CAMAAAD7OfD4AAAA1VBMVEX////9/v39/fz5/Pf4+/b1
+fH0+O/z+O7u9ejs9OTr9OPp8+Ho8t/k8Nnh7tXf7NHZ6cnX6MfW58XV58TT5sHS5b/A4P+/2qS7
2J+x05H/o6Oqz4enzIKiyXqZxW6Pv2CLvVqFuVJipSBgpB1foxteoxteoxpdohhboRVaoRRYoBJY
nxFUngxUnQxhikZeiURRmwdbiUJPmgRYiEFNmQJMmQA5j0Q5j0NDhTQjgCEhgCEggCAfgB8dHR0c
HBwbGxsQEBAODxAQDQ0MDhAQCgoJCQkAAABMoGFVAAAFI0lEQVR42u3dXYtVZRzG4Wfny0wziklF
ThqkNZFDiiedVgfhhy6IoC9QjBiN0NQUlKlRlijOW0jgwXIN69G193btdV/38R9/zsV2nNmw2JNi
L22TYi2DP/rBbx380Q9+6+CPfvBbB3/0g986+KMf/NbBH/3gtw7+6Ae/dfBHP/itgz/6teB/slxs
Bnv4TQX+9WIz2Rfw2zYo/G9L967erAle3qw4ulbKjYqzD7+qKX72dcXR9QZFxZ/VtwgfPnz48OHD
hw8fPnz48OHDhw8fPnz48OHDhw8fPnz48OHDhw8fPnz48OHDhw8fPnz48OHDhw8fPvzx4h+U7r1y
UGqu9iuOjr2MYtXZfpnW1bFK/LrX4cYUX/nzL9b9676yWaZ1dQ0+fPjw4cOHDx8+fPjw4cOHDx8+
fPjw4cOHH4//5qnyYlst5UHz73W4vwP/OfAvll74zW3Dfw78taUJ/DF8z78IHz58+PDhw4cPHz58
+PDhw4cPHz58+PDhw4c/XPyqx+tm+mzgo1KWZ1vcrTg7sVumdXViwM/hNovrpdyaZXHAz+HChw8f
Pnz48OHDhw8f/uLjv3Hu1VLKn3fuN1n7XMGvwn/nXPl/v/zeYO11Bb8Cf/lKubtdyunzpw+/222w
9rqC341/Ye3+1mEpZelq2bndYO11Bb8bf/21Oz+VJ7v0+h8/N1h7XcHvxv+4/PpbebIPztzeabD2
uoJf/6Pmqcvlx3sN1l5X8OvxN1b/2TposPa6Wlj8qW1yuLddg3/80pn9G49Lg7XP1eL+qDnN3arA
n2ys7P7wsDRY+1wt6i9Z756YN/7kvbO7m/ulydrjamHfXphmcb0K/+z7Zevv0sL6oleL+97O/PHX
LjzaLJ2s9VcL/Mba/PHPv/3v992s9Vfwn+J7Sxk+/Hb8leWDv7pZ66/g+54PH34H/urKwb1u1vor
+P7DhQ8fPnz48OHDHxq+TX/wjxj80e9Z/KF+XGnLPr9Z6h7O7n6g+qNBfI3w4cOHDx8+fPjw4cOH
Dx8+fPjw4cOHDx8+fPjww/HfWn5wF/688FsGHz58+PDhw4cPHz58+PDhw4cPHz58+PDhw4c/RfzH
pXsnG0c9rk5WFvdqisf3ao7m/zUu+Ct/dEX48DOL8OFnFuHDzyzCh59ZhA8/swgffmYRPvzMInz4
mUX48DOL8OFnFuHDzyzCh59ZhA8/swgffmYRPvzMInz4mUX48DOL8OFnFhfqacQFL3rlD6kIH35m
ET78zCJ8+JlF+PAzi/DhZxbhw88swoefWYQPP7MIH35mET78zCJ8+JlF+PAzi/DhZxbhw88swoef
WYQPP7MIH35mEf7g8G36g3/E4I9+vucPqQgffmYRPvzMInz4mUX48DOL8OFnFuHDzyzCh59ZhA8/
swgffmYRPvzMInz4mUX48DOL8OFnFuHDzyzCh59ZhA8/swgffmYR/uDwEz6p0GcjZhfhw88swoef
WYQPP7MIH35mET78zCJ8+JlF+PAzi/DhZxbhw88swoefWYQPP7MIH35mET78zCJ8+JlF+PAzi/Dh
Zxbhw88swoefWfQ0oqcRM4vw4WcW4cPPLMKHn1mEDz+zCB9+ZhE+/MwifPiZRfjwM4vw4WcW4cPP
LMKHn1mEDz+zCB9+ZhE+/MwifPiZRfjwM4vw4WcW4Q8O36Y/+EdsOPifLhWbwQ6/fBbf5jb4Axr8
1sEf/eC3Dv7oB7918Ec/+K2DP/rBbx380Q9+6+CPfvBbB3/0+w9gafNA+uY1rAAAAABJRU5ErkJg
gg==)

This type of logic is fairly time-consuming and error prone, but it's not really
that complex[^but-longer-than-expected], so we put together a Python program to
try out paths for us that satisfy the even-odd and uniqueness constraints. Given
that it was written hastily to solve a one-time problem, it's certainly neither
very neat nor readable, but it seems to do what we want!

[^but-longer-than-expected]: Over-optimistic as always, I think I had said we'd
    probably have a solution together in an hour. I think by the time we'd
    worked out all the bugs and edge cases, we were somewhere between three and
    four hours in, but it was a fun challenge to write!

<details>
<summary>Open if you dare!</summary>
{% highlight python %}
#!/usr/bin/python3
import copy
from time import sleep

# Originally these were just letters (X and O for even and odd snake, and x and
# o for even and odd empty cell), but as long as they're distinct, they do what
# we need. So these include ANSI color codes, which colors the snake red and
# blue.
EMPTY = "_"
ODD = "\033[34m_\033[0m"
EVEN = "\033[31m_\033[0m"
ODD_SNAKE = "\033[34mX\033[0m"
EVEN_SNAKE = "\033[31mX\033[0m"

# Here we define a few helper functions to make our lives easier later.
attempts = 0
def print_grid(grid):
    global attempts
    print(f"Attempt {attempts}:")
    attempts += 1
    for row in range(9):
        print(" ".join([r[row] for r in grid]))
    print()

def opposite_parity(x):
    if x == EVEN:
        return ODD
    else:
        return EVEN

def snake(x):
    if x == EVEN:
        return EVEN_SNAKE
    else:
        return ODD_SNAKE

def has_two_adjacent_snakes(grid, cell):
    """
    has_two_adjacent_snakes checks to see if two or more of the adjacent
    cells are filled with snake. If one is filled, we must be at the head of a
    snake; if two are filled we're along the body. No more than two can be
    filled, because then we'd have broken the snake; it would fork.
    """
    adjacent_snakes = 0
    if cell[1] > 0 and grid[cell[0]][cell[1] - 1] in [ODD_SNAKE, EVEN_SNAKE]: # north
        adjacent_snakes += 1

    if cell[0] < 8 and grid[cell[0] + 1][cell[1]] in [ODD_SNAKE, EVEN_SNAKE]: # east
        adjacent_snakes += 1

    if cell[1] < 8 and grid[cell[0]][cell[1] + 1] in [ODD_SNAKE, EVEN_SNAKE]: # south
        adjacent_snakes += 1
    
    if cell[0] > 0 and grid[cell[0] - 1][cell[1]] in [ODD_SNAKE, EVEN_SNAKE]: # west
        adjacent_snakes += 1
    return adjacent_snakes >= 2

def check_grid_parity(grid):
    """
    check_grid_parity employs a multi-pass approach. For each pass, it counts
    the even and odd cells in each row, column, and box. Then, if it has
    either four even or five odd cells, it knows that all of the others must be
    of the opposite parity, so it fills them in. This, however, may complete
    other rows/columns/boxes, so we'll do another pass after this one is done.
    We continue to do passes until either something breaks (returning False),
    or nothing is left to change.

    This is a lot of repetitive but just-slightly-different-each-time logic, so
    it can't easily be condensed. However, it's not particularly complicated,
    just rather verbose.
    """
    do_another_pass=False
    # check each row
    for row in grid:
        even_count = odd_count = 0
        for cell in row:
            if cell == EVEN or cell == EVEN_SNAKE:
                even_count += 1
            elif cell == ODD or cell == ODD_SNAKE:
                odd_count += 1
        if even_count > 4 or odd_count > 5:
            #print("broken on row")
            return False
        elif even_count == 4:
            for cell_index in range(len(row)):
                if row[cell_index] == EMPTY:
                    #print("filling row with odd")
                    row[cell_index] = ODD
                    do_another_pass=True
        elif odd_count == 5:
            for cell_index in range(len(row)):
                if row[cell_index] == EMPTY:
                    #print("filling row with even")
                    row[cell_index] = EVEN
                    do_another_pass=True

    # check each column
    for col_index in range(9):
        even_count = odd_count = 0
        for row in grid:
            if row[col_index] == EVEN or row[col_index] == EVEN_SNAKE:
                even_count += 1
            elif row[col_index] == ODD or row[col_index] == ODD_SNAKE:
                odd_count += 1
        #print(f"row {col_index}: even: {even_count}, odd: {odd_count}")
        if even_count > 4 or odd_count > 5:
            #print("broken on column")
            return False
        elif even_count == 4:
            for row in grid:
                if row[col_index] == EMPTY:
                    row[col_index] = ODD
                    #print("filling col with odd")
                    do_another_pass=True
        elif odd_count == 5:
            for row in grid:
                if row[col_index] == EMPTY:
                    row[col_index] = EVEN
                    #print("filling col with even")
                    do_another_pass=True

    # check each box
    for box_x in range(3):
        for box_y in range(3):
            even_count = odd_count = 0
            for x in range(3*box_x, 3*box_x+3):
                for y in range(3*box_y, 3*box_y + 3):
                    if grid[x][y] == EVEN or grid[x][y] == EVEN_SNAKE:
                        even_count += 1
                    elif grid[x][y] == ODD or grid[x][y] == ODD_SNAKE:
                        odd_count += 1
            if even_count > 4 or odd_count > 5:
                #print(f"bad parity on box {box_x},{box_y}")
                return False
            elif even_count == 4:
                for x in range(3*box_x, 3*box_x+3):
                    for y in range(3*box_y, 3*box_y + 3):
                        if grid[x][y] == EMPTY:
                            grid[x][y] = ODD
                            #print("filling box with odd")
                            do_another_pass=True
            elif odd_count == 5:
                for x in range(3*box_x, 3*box_x+3):
                    for y in range(3*box_y, 3*box_y + 3):
                        if grid[x][y] == EMPTY:
                            grid[x][y] = EVEN
                            #print("filling box with even")
                            do_another_pass=True

    if do_another_pass:
        return check_grid_parity(grid)
    else:
        return True

def has_adjacent_cells_of_parity(grid, cell, parity):
    adjacent_cells_of_parity = 0
    if cell[1] > 0 and grid[cell[0]][cell[1] - 1] == parity: # north
        adjacent_cells_of_parity += 1

    if cell[0] < 8 and grid[cell[0] + 1][cell[1]] == parity: # east
        adjacent_cells_of_parity += 1

    if cell[1] < 8 and grid[cell[0]][cell[1] + 1] == parity: # south
        adjacent_cells_of_parity += 1
    
    if cell[0] > 0 and grid[cell[0] - 1][cell[1]] == parity: # west
        adjacent_cells_of_parity += 1
    return adjacent_cells_of_parity > 0


def fill_empty_cells_around(grid, cell, value):
    """
    fill_empty_cells_around is applied to the "neck" (that is, the cell next to
    the head) of the snake. Supposing we have a snake like this, where E and O
    represent even and odd snake cells, and e and o non-snake cells:
        e o e _
        E O E O E
        e o e _
    then fill_empty_cells_around will be used with the above as `grid`, the
    last O in the row as `cell`, and "o" as `value`.
    """

    if cell[1] > 0 and grid[cell[0]][cell[1] - 1] == opposite_parity(value): # north
        raise ValueError
    elif cell[1] > 0 and grid[cell[0]][cell[1] - 1] == EMPTY: # north
        grid[cell[0]][cell[1] - 1] = value

    if cell[0] < 8 and grid[cell[0] + 1][cell[1]] == opposite_parity(value): # east
        raise ValueError
    elif cell[0] < 8 and grid[cell[0] + 1][cell[1]] == EMPTY: # east
        grid[cell[0] + 1][cell[1]] = value

    if cell[1] < 8 and grid[cell[0]][cell[1] + 1] == opposite_parity(value): # south
        raise ValueError
    elif cell[1] < 8 and grid[cell[0]][cell[1] + 1] == EMPTY: # south
        grid[cell[0]][cell[1] + 1] = value
    
    if cell[0] > 0 and grid[cell[0] - 1][cell[1]] == opposite_parity(value): # west
        raise ValueError
    elif cell[0] > 0 and grid[cell[0] - 1][cell[1]] == EMPTY: # west
        grid[cell[0] - 1][cell[1]] = value


def recursive_dfs(grid, head, neck, last_parity):

    # disable this if you don't want to see the solving visualization. Then you
    # can also disable the sleep(10) about 20 lines below, as we'll only be
    # printing the solutions.
    print_grid(grid)

    # check if we broke the grid:
    if not check_grid_parity(grid):
        return # try the next case

    # give the terminal a chance to keep up. On a 60hz display, this should
    # leave the grid on display for 1-2 frames.
    sleep(0.03)

    # base case: have we solved it (reached every box at least once)
    snakes_everywhere = True
    for box_x in range(3):
        for box_y in range(3):
            snake_in_grid = False
            for x in range(3*box_x, 3*box_x+3):
                for y in range(3*box_y, 3*box_y + 3):
                    if grid[x][y] in [ODD_SNAKE, EVEN_SNAKE]:
                        snake_in_grid = True
            if not snake_in_grid:
                snakes_everywhere = False
    if (snakes_everywhere and
        not has_adjacent_cells_of_parity(grid, head, opposite_parity(last_parity)) and
        not has_adjacent_cells_of_parity(grid, neck, last_parity)):
        print("Solved!")
        print_grid(grid)
        sleep(10) # give us a chance to look at what we found
        # note that we don't return here; we can try to see if there's a longer
        # snake that's also a solution.

    # if the cell is empty, then it doesn't have a parity, and therefore a snake
    # does not pass by in an adjacent cell, so it's a valid cell to try to enter
    #
    # For each of the directions (ordered north, east, south, and west), we make
    # sure we're not along that wall (if we're along the north wall, of course
    # we can't go north); we verify that either cell to the $direction of the
    # current head is empty (no constraints, so we can enter), or that it's the
    # same color as the one we're entering _and_ doesn't have two adjacent
    # snakes (that is, another besides the one we're entering from).
    #
    # If we have a neck cell (which we always do except on the very first cell
    # of the snake), we fill the cells around the neck with the appropriate
    # color. Note that we're filling the cells around the neck and not the
    # head. Although it does take one step longer to fail than would otherwise
    # be necessary, this saves us a lot of headache later: Say our head is even.
    # Then all of the cells around it except the neck cell (if applicable) and
    # the cell that will be the head next iteration (if the snake is not
    # complete) will also be even, to make the snake unambiguous. However, then
    # next iteration we will need to continue the snake into one of those even
    # cells---which one? Conversely, if we simply apply it to the neck after the
    # location of the new head has been decided, we avoid all this difficulty.
    #
    # We repeat this process for each possible direction.
    if head[1] > 0 and (grid[head[0]][head[1] - 1] == EMPTY or
        (grid[head[0]][head[1] - 1] == opposite_parity(last_parity) and
            not has_two_adjacent_snakes(grid, (head[0], head[1] - 1)))): # north
        new_grid = copy.deepcopy(grid)
        new_grid[head[0]][head[1] - 1] = snake(opposite_parity(last_parity))
        if neck is not None:
            try:
                fill_empty_cells_around(new_grid, neck, opposite_parity(last_parity))
            except ValueError:  # Cell is required to be both even and odd---abort!
                return # the neck is broken so this _can't_ be the head
        recursive_dfs(new_grid, (head[0], head[1] - 1), head, opposite_parity(last_parity))

    if head[0] < 8 and (grid[head[0] + 1][head[1]] == EMPTY or
        (grid[head[0] + 1][head[1]] == opposite_parity(last_parity) and
            not has_two_adjacent_snakes(grid, (head[0] + 1, head[1])))): # east
        new_grid = copy.deepcopy(grid)
        new_grid[head[0] + 1][head[1]] = snake(opposite_parity(last_parity))
        if neck is not None:
            try:
                fill_empty_cells_around(new_grid, neck, opposite_parity(last_parity))
            except ValueError:  # Cell is required to be both even and odd---abort!
                return
        recursive_dfs(new_grid, (head[0] + 1, head[1]), head, opposite_parity(last_parity))

    if head[0] > 0 and (grid[head[0] - 1][head[1]] == EMPTY or
        (grid[head[0] - 1][head[1]] == opposite_parity(last_parity) and
            not has_two_adjacent_snakes(grid, (head[0] - 1, head[1])))): # west
        new_grid = copy.deepcopy(grid)
        new_grid[head[0] - 1][head[1]] = snake(opposite_parity(last_parity))
        if neck is not None:
            try:
                fill_empty_cells_around(new_grid, neck, opposite_parity(last_parity))
            except ValueError:  # Cell is required to be both even and odd---abort!
                return
        recursive_dfs(new_grid, (head[0] - 1, head[1]), head, opposite_parity(last_parity))

    if head[1] < 8 and (grid[head[0]][head[1] + 1] == EMPTY or
        (grid[head[0]][head[1] + 1] == opposite_parity(last_parity) and
            not has_two_adjacent_snakes(grid, (head[0], head[1] + 1)))): # south
        new_grid = copy.deepcopy(grid)
        new_grid[head[0]][head[1] + 1] = snake(opposite_parity(last_parity))
        if neck is not None:
            try:
                fill_empty_cells_around(new_grid, neck, opposite_parity(last_parity))
            except ValueError:  # Cell is required to be both even and odd---abort!
                return
        recursive_dfs(new_grid, (head[0], head[1] + 1), head, opposite_parity(last_parity))

# We attempt to start in each cell in the grid, though to cut our search space
# and time in half, we constrain start_y <= start_x. Any snakes that would be
# found with start_y > start_x will be a mirror of one that will be found here.
# This still leaves quite a few duplicates by reflection and rotation, but those
# will be harder to weed out by simply adjusting the ranges here.
for start_x in range(9):
    for start_y in range(start_x + 1):
        empty_grid = []
        for i in range(9):
            empty_grid.append([EMPTY] * 9)
        empty_grid[start_x][start_y] = ODD_SNAKE
        recursive_dfs(empty_grid, (start_x, start_y), None, ODD)
{% endhighlight %}
</details>

While the rate my terminal emulator can display the text seems to currently be
the bottleneck, it's still certainly not slow, so I left the output displayed at
each step the algorithm takes. This was essential as a debugging tool, but now
it's just nice to watch it run. It's really a rather pretty visual; I forgot how
much time I could spend staring at visualizations of searches[^and-mazes]! If
I'm ever bored for an evening, I may consider porting it to Javascript so it can
run in the browser, but for now if you want to see more, you'll just have to
download and run it yourself. All you need is Python.

[^and-mazes]: If you also enjoy watching this sort of thing,
    [Jamis Buck's page on mazes](https://www.jamisbuck.org/mazes/) has a bunch
    of really neat animations!

<video autoplay loop style="display: block; margin: auto; padding: 20px;">
    <source src="/images/sudoku-animation.mp4" type="video/mp4">
</video>

A version of this program with all the print statements removed took about five
minutes to find 3241 possible configurations that satisfied the constraints.

Since we've found all the possible combinations (recognized by this program, at
least), we can also figure out the shortest and longest possible paths that
satisfy the constraints---21 and 37, respectively. And both are pretty neat
shapes!
<div style="display: flex; flex-wrap: wrap; justify-content: center;">
    <img alt="the shortest path" src="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAXwAAAF8CAMAAAD7OfD4AAAAV1BMVEX////A4P//o6NPnWJPnGFM
m15KmVtAk0w5j0Q5j0NMhjo3jkBEhTVDhTRAhDMigSMigSIggCAfgB8dHR0cHBwbGxsQEBAODxAQ
DQ0MDhAQCgoJCQkAAACyLBS2AAAED0lEQVR42u3d227TQBSG0TacS1uYAZq65P2fE6vcQSN+RduD
7a7vOsp2lsb2TUZzJUmSJEmSJEmSJEn/7PtJS/QtwT9pmeC/2KrwD0HTddLTISi8sGzicfhvjD4F
Hz58+PDhw4cPHz58+PDhw4cPHz58+PDhw4cPHz58+PDhw4cPHz58+PDhw4cPHz58+PDhw4cPHz78
HeNPQaenpOhT6cSp7Lpqf+MUlONnazop+lQ4sfBeK/2N0XXBhw8fPnz48OHDhw8fPnz48OHDhw8f
Pnz48OHDhw8fPnz48OHDhw8fPnz48OHDhw8fPnz48OHDhw8fPvxy/Nq9gVPQevc/1k2sXfmFe1RX
e68VToQPHz58+PDhw4cPHz58+PDhw4cPHz58+PDh7xn/TXu3Yfz79lfzxHZRvd2Nxm/t64bxW4Kf
Nx6/wYd/IX7ZMx8+fPjw4cOHDx8+fPjw4cOHDx8+fPjw4cNfD77Kg38u+LsvxE+edLUbhA9B6cTg
jRX/Pabs7QcfPnz48OHDhw8fPnz48OHDhw8fPnz48OEvjt9bXyX+fUuqxJ8lrPzftaiNr/xt4/f+
Af4i+NlE+PDhw4cPHz58+PDhw4cPHz58+PDhw4cPHz78Jc9GbK1deDZi6UmFU9l1zRMvO/WwtTb6
bMTW2oAzOseuw0PQxnegw4cPHz58+PDhw4cPHz58+PDhw4cPHz58+PBH4ffW4T83S1j5r2jlrxW/
9w7fyocPHz58+PDhw4cPHz58+PDhw4cPHz58+PDhvyr8aA/eFBTvDZyCsr2B4/c/RhNr9+GOP5I1
W4fj77VoInz48OHDhw8fPnz48OHDhw8fPnz48OHDhw9/5/hBvX0qw//cksbjpxJ3hfhpZfht0/hz
dfi3K8Xv/WYw/scB+EG1/yUoeLYOwE/fRfDhw4cPHz58+PDhw4cPHz58+PDhw4cPH/7y+Fog+OeC
v/sS/PEHpI4/BLb0mR+9/eDDhw8fPnz48OHDhw8fPnz48OHDhw8fPvz14F/WPLH9EXz428G/LcTv
/WbD+O+/vB2AX0Px8sQN48/Bhw8fPnz48OHDhw8fPnz48OHDhw8fPnz48PeMn51UmJSejZh9V9Lp
GJROPCZF15XjXweNX/nZOjwW3t2PV0nRdcGHDx8+fPjw4cOHDx8+fPjw4cOHDx8+fPjw4cOHDx8+
fPjw4cOHDx8+fPjw4cOHDx8+fPjw4cOHDx8+/Of+x27EqWzP4jzxMSic+BCU7kZ8SIq+KsQvPq40
KLywta786DfChw8fPnz48OHDhw8fPnz48OHDhw8fPnz48OHDhw8fPnz48OHDhw8fPnz48OHDhw8f
Pnz48OHDhw9/x/gqD/651oP/46Ql+nklSZIkSZIkSZK21y+/uqs0tU7NAQAAAABJRU5ErkJggg==">
    <img alt="the longest path"  src="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAXwAAAF8CAMAAAD7OfD4AAAAVFBMVEX////A4P//o6NNm19Mml5J
mFlIl1hAk0w5j0Q5j0NMhjo3jkA2jkBEhjREhTVDhTRAhTJAhDMhgCEggCAfgB8dHR0cHBwbGxsM
DhAQCgoJCQkAAABTFEzFAAAEVUlEQVR42u3d3W4aMRCA0dC/NKRJ24zbQnn/9+xKzVWAZLKaBRvO
d72S2SPjGzT4RpIkSZIkSZIkSZLe7PdOS/Qrg7/TMsE/WFf4q0TbD5k2q0TJFTerss9V+o6pp+DD
hw8fPnz48OHDhw8fPnz48OHDhw8fPvzF8T9FXS3uyvDvY2bTinM//fdT40dtZfiRKImf79T4X57i
leAPc+YX45/4zIcPHz58+PDhw4cPHz58+PDhw4cPHz58+PDhw58e2yTabTPtPxUR2xfNXjEiEitO
zVxx/6GIOPBUonPs/IN7p4t9WPdd26wSwYcPHz58+PDhw4cPHz58+PDhw4cPHz58+PDh5/B7mZCa
h9+iwf+fnf9O/MdC/NbW8I/X7zw4fPjw4Xe4Inz48OHDhw8fPnz48OHDhw8fPnz48EfBz03qlc0s
ls4/ZmcDy2Ypt5XTiIP/s3F2H87+BXreivDhw4cPHz58+PDhw4cPHz58+PDhw4cPHz58+FeCn6jF
HfwF8LPBr8d/hH8e/PyK8OHDhw8fPnz48OHDhw8fPnz48OHDhw8f/vL4WiD4x4J/8Z3hStZEg694
8Gf2Pu/DhQ8fPnz48MddET58+PDhw4cPHz58+PDhw4ffJf59VPb5xPgt2sj4UdqTnX8+/I/w34nv
zIcPHz58+PDhw4cPHz58+PDhw4cPHz58+PDh94qfu4MwU/bewMwdhIV3Iy78jhEx/27Eqh2WvzEz
85/FhTu/+B0T31v48OHDhw8fPnz48OHDhw8fPnz48OHDhw8fPvzcB7uPvaYV40Vj47dofeLHFeB3
u/Nz+K2t4S/ywXIU8OHDhw8fPnz48OHDhw8fPnz48OHDhw8fPnz4veIXTuptE3OG55h/TD1W+o6n
3/mpGdXSFSvncAvfET58+PDhw4cPHz58+PDhw4cPHz58+PDhw4d/yfg/o66x8b9Fi0SV+AH/uYgY
Gb+19RXgr0vxy878qbHxc+8IHz58+PDhw4cPHz58+PDhw4cPHz58+PDhL4yvBYJ/LPgXXxI/c9LV
nvmrRLVnfsllq/nhbPjw4cOHDx8+fPjw4cOHDx8+fPjw4cOHDx/+yfBbNPhXtPNba/AdO/Dhw4cP
Hz58+PDhw4cPHz58+PDhw4cPHz58+B3gJ+76q7ypsPg2xkSzV4yIee9YOwS9+D7scux69hkAHz58
+PDhw4cPHz58+PDhw4cPHz58+PDhw79w/FRfB8b/ES3ermP8GBg/IvrEf2gN/nO3p8TPUwyPn1sR
Pnz48OHDhw8fPnz48OHDhw8fPnz48OHDhw9/m2i3zcws9juNWDFnWD+NWDqj2u/Oz3xvuz124MOH
Dx8+fPjw4cOHDx8+fPjw4cOHDx8+fPiD4s9rWjFmVbki/P3g5/AfWhsa/3Zk/KmBz/wp+PDhw4cP
Hz58+PDhw4cPHz58+PDhw4cPfyh8lQf/WP3g/9lpif7eSJIkSZIkSZKk8foHK448QtxiyygAAAAA
SUVORK5CYII=">
</div>

<div class="light">
    Images from this post were created using 
    <a href="https://swaroopg92.github.io/penpa-edit/">penpa-edit</a>.
</div>
