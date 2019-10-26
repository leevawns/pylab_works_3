Vmax = 5
Vmin = 0
Vold = 2.5
Btc = 36 #0.1393 * 0.632

bert_bitlist = []
bert_list = []
for frame in data:
#  frame = frame / 256.0 * 5.0
  hi = Vold + (Vmax - Vold) / Btc
  lo = Vold + (Vmin - Vold) / Btc
  if abs(frame - hi) < abs(frame - lo):
    # Hi bit
    bert_bitlist.append(1)
    Vold = hi
  else:
    bert_bitlist.append(0)
    Vold = lo
  bert_list.append(Vold)

DISPLAY = data, bert_list

Display_Params = []
Display_Params.append (['org', Auto ])
Display_Params.append (['T1',2,3])
