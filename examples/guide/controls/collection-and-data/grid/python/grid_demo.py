from easyvrui import grid, grid_column, label, rect, run, window

def main():
    window_main = window("window_main")
    window_main.title = "编辑同步参数"
    window_main.set_size(680, 390)
    grid_config = grid("grid_config")
    grid_config.rect = rect(36, 85, 608, 165)
    grid_config.column_list = [grid_column("参数", 270, False), grid_column("值", 210, True)]
    grid_config.row_count = 2
    grid_config[0, 0] = "并行任务"
    grid_config[0, 1] = 4
    grid_config[1, 0] = "重试次数"
    grid_config[1, 1] = 2
    label_state = label("label_state")
    label_state.rect = rect(36, 282, 608, 46)
    label_state.text = "双击值所在单元格进行编辑"

    def grid_config_edit_committed(source, event):
        label_state.text = "参数修改已提交"

    grid_config.on_edit_committed += grid_config_edit_committed
    window_main.control_list.add(grid_config)
    window_main.control_list.add(label_state)
    window_main.show()
    run("tutorial_grid")

if __name__ == "__main__":
    main()