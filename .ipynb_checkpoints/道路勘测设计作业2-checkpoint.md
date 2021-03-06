# **道路勘测设计**

## 第二章作业

### 2-2 为何要限制直线的长度？

- 直线的最大长度
  - 在地形起伏较大的地区，直线难以与地形相适应，易产生高填深挖路基，破坏自然景观。
  - 若长度运用不当，会影响线形的连续性。
  - 过长的直线会使驾驶员感到单调、疲倦和急躁，难以目测车间距离，增加夜间行车车灯炫目的危险，还会激发超速行驶，从而导致交通事故的发生。
- 直线的最小长度
  - 曲线间的过短直线容易造成视觉不连续、驾驶员操纵困难等问题。
  - 同向曲线间的直线较短时，在视觉上容易产生把直线与两端曲线看成为反向曲线的错觉；当直线过短时甚至把两个曲线看成是一个曲线，破坏了线形的连续性，易造成驾驶操作失误。
  - 反向曲线两弯道转弯方向相反，考虑超高和加宽过渡的需要，以及驾驶员操作的方便，其间直线的最小长度应予限制。

### 2-3 公路的最小圆曲线半径有几种？分别在何种情况下使用？

- 极限最小半径
  - 为保证车辆按设计速度安全行驶所规定的圆曲线半径最小值。
  - 地形条件特殊困难不得已时，方可采用圆曲线极限最小半径。
- 一般最小半径
  - 各级公路对按设计速度行驶的车辆能保证其安全、舒适的最小圆曲线半径。
  - 通常情况下推荐采用。
- 不设超高的最小半径
  - 指不必设置超高就能满足行驶稳定性的圆曲线最小半径。
    - 汽车在这种圆曲线上以设计速度或以接近设计速度行驶时，旅客有充分的舒适感。
    - 地形比较复杂的情况下不会过多增加工程量。
  - 圆曲线半径较大时，离心力的影响较小，路面摩阻力可保证汽车有足够的稳定性，这时可不设超高，设置与直线段上相同的双向横坡路拱形式。

### 2-4 缓和曲线的作用是什么？确定其长度应考虑哪些因素？

- 缓和曲线的作用
  - 曲率连续变化，便于车辆遵循
    - 从安全性考虑，有必要设置一条驾驶员易于遵循的缓和曲线，使车辆在进入或离开圆曲线时不致侵入邻近的车道。
  - 离心加速度逐渐变化，旅客感觉舒适
    - 在曲率不同的直线和圆曲线、圆曲线和圆曲线之间，设置一条过渡性的曲线以缓和离心加速度的变化，减轻曲率的突变带给乘客的不舒适的感觉。
  - 超高及加宽逐渐变化，行车更加平稳
    - 为避免车辆在从直线上的双坡断面过渡到圆曲线上的单坡断面和由直线上的正常宽度过渡到圆曲线上的加宽宽度时急剧地左右摇摆，并保证路容的美观，需设置一定长度的缓和曲线。
  - 与圆曲线配合，增加线形美观
    - 设置缓和曲线后，线形连续圆滑，增加线形的美观，同时从外观上看也感到安全。
- 确定其长度应考虑

  - 旅客感觉舒适
    - 离心加速度变化过快会使乘客感到横向冲击
    - $ L_s(min)=0.0214\frac{\nu^3}{R\alpha_s} $ 
    - $ \alpha_s $ 为离心加速度变化率，我国一般控制在$0.5\sim0.6m/s^3 $范围内。
  - 超高渐变率适中
    - 超高过渡段太短会使路面急剧地由双坡变为单坡，形成一种扭曲的面，对行车和路容均不利（同时还有考虑排水问题）
    - $ L_s(min)=\frac{B'\Delta i}{p} $ 
    - $ B' $ 为旋转轴至边缘宽度，$\Delta i$为超高与路拱坡度差，*p* 为超高渐变率
  - 行驶时间不过短
    - 行驶时间过短会使驾驶员操作不便，甚至造成驾驶操纵的紧张和忙乱
    - 汽车在缓和曲线上的行驶时间至少应达到$3s$ 
    - $ L_s(min)=\frac{\nu}{1.2} $ 
    - $\nu$为汽车行驶速度（km/h）
- 除此之外，还应注意与直线和圆曲线相协调、配合，在线形组合和线形美观上产牛良好的行车和视觉效果。

### 2-6 某丘陵区公路，设计速度为$40km/h$，如图，路线转角$α_{4右}$=95°04′38″，$α_{5左}$=69°20′28″，$JD_4$至$JD_5$的距离$D=267.71m$。由于地形限制，选定$R_4=110m$、$L_{S4}=70m$,试定$JD_5$的圆曲线半径$R_5$和缓和曲线长$L_{s5}$。

![图片2](道路勘测设计作业2.assets/图片2-1584869174571.png)

解：

- 对于前一个曲线，计算平面线要素
  - 切线增长值：$q=\frac{L_{s4}}{2}-\frac{L_{s4}^3}{240R_4^2}=34.88m$ 
  - 内移值：$p=\frac{L_{s4}^2}{24R_4}-\frac{L_{s4}^4}{2688R_4^3}=1.85m$ 
  - 切线长：$ T_4=(R_4+p)tan\frac{\alpha_{4右}}{2}+q=157.11m $ 
- 若在反向曲线间设置直线
  - 反向曲线间直线的最小长度
    - 设计速度$=40km/h$，直线最小长度为$L=80m$ 
  - 两曲线反向回旋线以径向连接，切线长加上直线长为间距
    - 切线长：$T_5=D-T_4-L=30.60m$ 
  - 对于后一个曲线，缓和曲线最小长度为
    - $min\ L_{s5}=max(0.0214\frac{\nu^3}{R\alpha_s},\frac{B'\Delta i}{p},\frac{\nu}{1.2},15b)\ge\frac{\nu}{1.2}=33.33m$ 
  - 显然$min\ L_{s5}>T_5 $，布设失败
- 设置S形曲线
  - 切线长：$T_5=D-T_4=110.60m$ 
  - 从行驶力学与线形协调、超高过渡考虑，S形曲线相邻两回旋线参数宜相等
    - $ T_5\approx(R_5+\frac{L_{s5}^2}{24R_5})tan\frac{\alpha_{5左}}{2}+\frac{L_{s5}}{2}$ 
    - $R_4L_{S4}=R_5L_{S5}$ 
  - 解得$R_5=64.63m,L_{s5}=119.132m$，或$R_5=104.44m,L_{s5}=73.73m$ 
    - ![图片3](道路勘测设计作业2.assets/图片3.png)
  - 半径之比均满足$R_2/R_1=1/3\sim1$，不宜过大，则选择半径差值较小的一组
- $R_5=104.44m,L_{s5}=73.73m$ 

> Sofarja@outlook.com
>
> ---
>
> 21018116
>
> 郭艺铧
>
> 交通工程

