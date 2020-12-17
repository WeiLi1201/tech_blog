linelist = []
        with open("time.csv","r",encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                splits = line.split(',')
                for i in range(0,5):
                    begin_time = str(datetime.fromtimestamp(int(splits[0])))
                    begin_time = datetime.strptime(begin_time, "%Y-%m-%d %H:%M:%S")
                    output_time = begin_time + timedelta(minutes=i)
                    print(f'{output_time},{splits[1]}')
                    linelist.append(f'{output_time},{splits[1]}')

        with open("def.csv","w+",encoding="utf-8") as w:
            w.writelines([line for line in linelist])
