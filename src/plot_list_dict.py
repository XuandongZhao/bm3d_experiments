from matplotlib import pyplot as plt


def plot_dict_res(*line_dicts, im_label='im_label', x_lable='x_lable', y_label='y_label'):
    for dict_i, diction in enumerate(line_dicts):
        isinstance(diction, dict)
        label = diction['name']
        x_list = diction['x']
        y_list = diction['y']
        color = diction.get('color')
        linestyle = diction.get('linestyle')

        if linestyle is None:
            linestyle = '--'
        if color is None:
            color = 'black'

        plt.plot(x_list, y_list, color=color, linestyle=linestyle, label=label)
        for x__, y__ in zip(x_list, y_list):
            plt.annotate('%.4f' % y__,  # this is the text
                         (x__, y__),  # this is the point to label
                         textcoords="offset points",  # how to position the text
                         xytext=(8*dict_i, 7*dict_i),  # distance from text to points (x,y)
                         ha='center',# horizontal alignment can be left, right or center
                         color=color,
                         fontsize=7)

                # plt.text(x__, y__, '%.4f' % y__, ha='center', va='bottom', fontsize=10, color=color)

    plt.rcParams['savefig.dpi'] = 300  # 图片像素
    plt.rcParams['figure.dpi'] = 300  # 分辨率
    plt.title(im_label)
    plt.xlabel(x_lable)
    plt.ylabel(y_label)
    plt.legend()
    return plt


if __name__ == '__main__':
    k_ = ['name', 'x', 'y', 'color', 'linestyle']
    x_list = [1, 2, 3, 4, 5]
    y_list = [7, 2, 0, 4, 5]
    v_ = ['test', x_list, y_list, 'gold', '--']
    line_dict = dict(zip(k_, v_))

    pltt = plot_dict_res(line_dict)
    pltt.show()
