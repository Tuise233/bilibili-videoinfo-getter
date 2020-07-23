#Bilibili AV号、BV号转换

class BvConvert:

    def  bv2av(self,bv):
        table='fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
        tr={}
        for i in range(58):
            tr[table[i]]=i
        s=[11,10,3,8,4,6]
        xor=177451812
        add=8728348608
        r=0
        for i in range(6):
            r+=tr[bv[s[i]]]*58**i
        return (r-add)^xor

    def av2bv(self,av):
        table='fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
        tr={}
        for i in range(58):
            tr[table[i]]=i
        s=[11,10,3,8,4,6]
        xor=177451812
        add=8728348608
        av=(av^xor)+add
        r=list('BV1  4 1 7  ')
        for i in range(6):
            r[s[i]]=table[av//58**i%58]
        return ''.join(r)
