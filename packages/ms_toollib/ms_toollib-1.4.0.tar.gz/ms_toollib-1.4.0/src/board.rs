﻿use ms_toollib::*;
use pyo3::prelude::*;
use itertools::Itertools;

#[pyclass(name = "MinesweeperBoard")]
pub struct PyMinesweeperBoard {
    pub core: MinesweeperBoard,
}

#[pymethods]
impl PyMinesweeperBoard {
    #[new]
    pub fn new(board: Vec<Vec<i32>>) -> PyMinesweeperBoard {
        let c = MinesweeperBoard::new(board.clone());
        PyMinesweeperBoard { core: c }
    }
    pub fn step(&mut self, e: &str, pos: (usize, usize)) {
        self.core.step(e, pos).unwrap();
    }
    pub fn reset(&mut self) {
        self.core.reset();
    }
    pub fn step_flow(&mut self, operation: Vec<(&str, (usize, usize))>) {
        self.core.step_flow(operation).unwrap();
    }
    // 这个方法与强可猜、弱可猜有关
    #[setter]
    fn set_board(&mut self, board: Vec<Vec<i32>>) {
        self.core.board = board;
    }
    // 直接设置游戏局面是不安全的！但在一些游戏中，结束时需要修改再展示
    #[setter]
    fn set_game_board(&mut self, game_board: Vec<Vec<i32>>) {
        self.core.game_board = game_board;
    }
    #[getter]
    fn get_board(&self) -> PyResult<Vec<Vec<i32>>> {
        Ok(self.core.board.clone())
    }
    #[getter]
    fn get_game_board(&self) -> PyResult<Vec<Vec<i32>>> {
        Ok(self.core.game_board.clone())
    }
    fn get_game_board_2(&self, mine_num: f64) -> PyResult<Vec<Vec<Vec<f64>>>> {
        // 返回用于强化学习的局面，即状态
        let mut game_board_clone = self.core.game_board.clone();
        let t_1: Vec<Vec<f64>> = game_board_clone
            .iter()
            .map(|x| x.iter().map(|x| {
                        if *x == 10 {
                            return -1;
                        } else if *x == 11 {
                            return -2;
                        } else {
                            return *x
                        }
                    }).map(|y| y as f64).collect::<Vec<f64>>())
            .collect_vec();
        // 把玩家或ai标的错的雷都删了
        game_board_clone.iter_mut().for_each(|x| {
            x.iter_mut().for_each(|x| {
                if *x > 10 {
                    *x = 10
                }
            })
        });
        mark_board(&mut game_board_clone);
        let (t_2, _) = cal_possibility_onboard(&game_board_clone, mine_num).unwrap();
        let t = vec![t_1, t_2];
        Ok(t)
    }
    #[getter]
    fn get_left(&self) -> PyResult<usize> {
        Ok(self.core.left)
    }
    #[getter]
    fn get_right(&self) -> PyResult<usize> {
        Ok(self.core.right)
    }
    #[getter]
    fn get_chording(&self) -> PyResult<usize> {
        Ok(self.core.chording)
    }
    #[getter]
    fn get_ces(&self) -> PyResult<usize> {
        Ok(self.core.ces)
    }
    #[getter]
    fn get_flag(&self) -> PyResult<usize> {
        Ok(self.core.flag)
    }
    #[getter]
    fn get_solved3BV(&self) -> PyResult<usize> {
        Ok(self.core.solved3BV)
    }
    #[getter]
    fn get_row(&self) -> PyResult<usize> {
        Ok(self.core.row)
    }
    #[getter]
    fn get_column(&self) -> PyResult<usize> {
        Ok(self.core.column)
    }
    #[getter]
    fn get_game_board_state(&self) -> PyResult<usize> {
        match self.core.game_board_state {
            GameBoardState::Ready => Ok(1),
            GameBoardState::Playing => Ok(2),
            GameBoardState::Win => Ok(3),
            GameBoardState::Loss => Ok(4),
        }
    }
    #[getter]
    fn get_mouse_state(&self) -> PyResult<usize> {
        match self.core.mouse_state {
            MouseState::UpUp => Ok(1),
            MouseState::UpDown => Ok(2),
            MouseState::UpDownNotFlag => Ok(3),
            MouseState::DownUp => Ok(4),
            MouseState::Chording => Ok(5),
            MouseState::ChordingNotFlag => Ok(6),
            MouseState::DownUpAfterChording => Ok(7),
            MouseState::Undefined => Ok(8),
        }
    }
}

#[pyclass(name = "AvfVideo")]
pub struct PyAvfVideo {
    pub core: AvfVideo,
}

#[pymethods]
impl PyAvfVideo {
    #[new]
    pub fn new(file_name: &str) -> PyAvfVideo {
        let c = AvfVideo::new(file_name);
        PyAvfVideo { core: c }
    }
    pub fn parse_video(&mut self) {
        self.core.parse_video().unwrap();
    }
    pub fn analyse(&mut self) {
        self.core.data.analyse();
    }
    pub fn analyse_for_features(&mut self, controller: Vec<&str>) {
        self.core.data.analyse_for_features(controller);
    }
    #[getter]
    fn get_row(&self) -> PyResult<usize> {
        Ok(self.core.data.height)
    }
    #[getter]
    fn get_column(&self) -> PyResult<usize> {
        Ok(self.core.data.width)
    }
    #[getter]
    fn get_level(&self) -> PyResult<u8> {
        Ok(self.core.data.level)
    }
    #[getter]
    fn get_win(&self) -> PyResult<bool> {
        Ok(self.core.data.win)
    }
    #[getter]
    fn get_mine_num(&self) -> PyResult<usize> {
        Ok(self.core.data.mine_num)
    }
    #[getter]
    fn get_player(&self) -> PyResult<String> {
        Ok(self.core.data.player.clone())
    }
    #[getter]
    fn get_bbbv(&self) -> PyResult<usize> {
        Ok(self.core.data.static_params.bbbv)
    }
    #[getter]
    fn get_start_time(&self) -> PyResult<String> {
        Ok(self.core.data.start_time.clone())
    }
    #[getter]
    fn get_openings(&self) -> PyResult<usize> {
        Ok(self.core.data.static_params.openings)
    }
    #[getter]
    fn get_islands(&self) -> PyResult<usize> {
        Ok(self.core.data.static_params.islands)
    }
    #[getter]
    fn get_hizi(&self) -> PyResult<usize> {
        Ok(self.core.data.static_params.hizi)
    }
    #[getter]
    fn get_cell0(&self) -> PyResult<usize> {
        Ok(self.core.data.static_params.cell0)
    }
    #[getter]
    fn get_cell1(&self) -> PyResult<usize> {
        Ok(self.core.data.static_params.cell1)
    }
    #[getter]
    fn get_cell2(&self) -> PyResult<usize> {
        Ok(self.core.data.static_params.cell2)
    }
    #[getter]
    fn get_cell3(&self) -> PyResult<usize> {
        Ok(self.core.data.static_params.cell3)
    }
    #[getter]
    fn get_cell4(&self) -> PyResult<usize> {
        Ok(self.core.data.static_params.cell4)
    }
    #[getter]
    fn get_cell5(&self) -> PyResult<usize> {
        Ok(self.core.data.static_params.cell5)
    }
    #[getter]
    fn get_cell6(&self) -> PyResult<usize> {
        Ok(self.core.data.static_params.cell6)
    }
    #[getter]
    fn get_cell7(&self) -> PyResult<usize> {
        Ok(self.core.data.static_params.cell7)
    }
    #[getter]
    fn get_cell8(&self) -> PyResult<usize> {
        Ok(self.core.data.static_params.cell8)
    }
    #[getter]
    fn get_r_time(&self) -> PyResult<f64> {
        Ok(self.core.data.dynamic_params.r_time)
    }
    #[getter]
    fn get_r_time_ms(&self) -> PyResult<u32> {
        Ok(self.core.data.dynamic_params.r_time_ms)
    }
    #[getter]
    fn get_bbbv_s(&self) -> PyResult<f64> {
        Ok(self.core.data.dynamic_params.bbbv_s)
    }
    #[getter]
    fn get_stnb(&self) -> PyResult<f64> {
        Ok(self.core.data.dynamic_params.stnb)
    }
    #[getter]
    fn get_rqp(&self) -> PyResult<f64> {
        Ok(self.core.data.dynamic_params.rqp)
    }
    #[getter]
    fn get_lefts(&self) -> PyResult<usize> {
        Ok(self.core.data.dynamic_params.lefts)
    }
    #[getter]
    fn get_rights(&self) -> PyResult<usize> {
        Ok(self.core.data.dynamic_params.rights)
    }
    #[getter]
    fn get_chordings(&self) -> PyResult<usize> {
        Ok(self.core.data.dynamic_params.chordings)
    }
    #[getter]
    fn get_clicks(&self) -> PyResult<usize> {
        Ok(self.core.data.dynamic_params.clicks)
    }
    #[getter]
    fn get_flags(&self) -> PyResult<usize> {
        Ok(self.core.data.dynamic_params.flags)
    }
    #[getter]
    fn get_ces(&self) -> PyResult<usize> {
        Ok(self.core.data.dynamic_params.ces)
    }
    #[getter]
    fn get_lefts_s(&self) -> PyResult<f64> {
        Ok(self.core.data.dynamic_params.lefts_s)
    }
    #[getter]
    fn get_rights_s(&self) -> PyResult<f64> {
        Ok(self.core.data.dynamic_params.rights_s)
    }
    #[getter]
    fn get_chordings_s(&self) -> PyResult<f64> {
        Ok(self.core.data.dynamic_params.chordings_s)
    }
    #[getter]
    fn get_clicks_s(&self) -> PyResult<f64> {
        Ok(self.core.data.dynamic_params.clicks_s)
    }
    #[getter]
    fn get_ces_s(&self) -> PyResult<f64> {
        Ok(self.core.data.dynamic_params.ces_s)
    }
    #[getter]
    fn get_ioe(&self) -> PyResult<f64> {
        Ok(self.core.data.dynamic_params.ioe)
    }
    #[getter]
    fn get_thrp(&self) -> PyResult<f64> {
        Ok(self.core.data.dynamic_params.thrp)
    }
    #[getter]
    fn get_corr(&self) -> PyResult<f64> {
        Ok(self.core.data.dynamic_params.corr)
    }
    #[getter]
    fn get_events_len(&self) -> PyResult<usize> {
        Ok(self.core.data.events.len())
    }
    pub fn events_time(&self, index: usize) -> PyResult<f64> {
        Ok(self.core.data.events[index].time)
    }
    pub fn events_mouse(&self, index: usize) -> PyResult<String> {
        Ok(self.core.data.events[index].mouse.clone())
    }
    pub fn events_x(&self, index: usize) -> PyResult<u16> {
        Ok(self.core.data.events[index].x)
    }
    pub fn events_y(&self, index: usize) -> PyResult<u16> {
        Ok(self.core.data.events[index].y)
    }
    pub fn events_useful_level(&self, index: usize) -> PyResult<u8> {
        Ok(self.core.data.events[index].useful_level)
    }
    pub fn events_prior_game_board(&self, index: usize) -> PyResult<PyGameBoard> {
        let mut t = PyGameBoard::new(self.core.data.mine_num);
        // t.set_core(self.core.data.events[index].prior_game_board.clone());
        t.set_core(self.core.data.game_board_stream[self.core.data.events[index].prior_game_board_id].clone());
        Ok(t)
    }
    pub fn events_comments(&self, index: usize) -> PyResult<String> {
        Ok(self.core.data.events[index].comments.clone())
    }
    pub fn events_mouse_state(&self, index: usize) -> PyResult<usize> {
        match self.core.data.events[index].mouse_state {
            MouseState::UpUp => Ok(1),
            MouseState::UpDown => Ok(2),
            MouseState::UpDownNotFlag => Ok(3),
            MouseState::DownUp => Ok(4),
            MouseState::Chording => Ok(5),
            MouseState::ChordingNotFlag => Ok(6),
            MouseState::DownUpAfterChording => Ok(7),
            MouseState::Undefined => Ok(8),
        }
    }
    #[getter]
    pub fn get_current_event_id(&self) -> PyResult<usize> {
        Ok(self.core.data.current_event_id)
    }
    #[setter]
    pub fn set_current_event_id(&mut self, id: usize) {
        self.core.data.current_event_id = id
    }
    #[getter]
    pub fn get_game_board(&self) -> PyResult<Vec<Vec<i32>>> {
        Ok(self.core.data.get_game_board())
    }
    #[getter]
    pub fn get_game_board_poss(&mut self) -> PyResult<Vec<Vec<f64>>> {
        Ok(self.core.data.get_game_board_poss())
    }
    #[getter]
    pub fn get_mouse_state(&self) -> PyResult<usize> {
        match self.core.data.events[self.core.data.current_event_id].mouse_state {
            MouseState::UpUp => Ok(1),
            MouseState::UpDown => Ok(2),
            MouseState::UpDownNotFlag => Ok(3),
            MouseState::DownUp => Ok(4),
            MouseState::Chording => Ok(5),
            MouseState::ChordingNotFlag => Ok(6),
            MouseState::DownUpAfterChording => Ok(7),
            MouseState::Undefined => Ok(8),
        }
    }
    /// 局面状态（录像播放器的局面状态始终等于1，没有ready、win、fail的概念）
    #[getter]
    pub fn get_game_board_state(&self) -> PyResult<usize> {
        Ok(1)
    }
    /// 返回当前光标的位置，播放录像用
    #[getter]
    pub fn get_x_y(&self) -> PyResult<(u16, u16)> {
        Ok((
            self.core.data.events[self.core.data.current_event_id].x,
            self.core.data.events[self.core.data.current_event_id].y,
        ))
    }
    #[setter]
    pub fn set_time(&mut self, time: f64) {
        self.core.data.set_current_event_time(time);
    }
}





#[pyclass(name = "RmvVideo")]
pub struct PyRmvVideo {
    pub core: RmvVideo,
}

#[pymethods]
impl PyRmvVideo {
    #[new]
    pub fn new(file_name: &str) -> PyRmvVideo {
        let c = RmvVideo::new(file_name);
        PyRmvVideo { core: c }
    }
    pub fn parse_video(&mut self) {
        self.core.parse_video().unwrap();
    }
    pub fn analyse(&mut self) {
        self.core.data.analyse();
    }
    pub fn analyse_for_features(&mut self, controller: Vec<&str>) {
        self.core.data.analyse_for_features(controller);
    }
    #[getter]
    fn get_row(&self) -> PyResult<usize> {
        Ok(self.core.data.height)
    }
    #[getter]
    fn get_column(&self) -> PyResult<usize> {
        Ok(self.core.data.width)
    }
    #[getter]
    fn get_level(&self) -> PyResult<u8> {
        Ok(self.core.data.level)
    }
    #[getter]
    fn get_win(&self) -> PyResult<bool> {
        Ok(self.core.data.win)
    }
    #[getter]
    fn get_mine_num(&self) -> PyResult<usize> {
        Ok(self.core.data.mine_num)
    }
    #[getter]
    fn get_player(&self) -> PyResult<String> {
        Ok(self.core.data.player.clone())
    }
    #[getter]
    fn get_bbbv(&self) -> PyResult<usize> {
        Ok(self.core.data.static_params.bbbv)
    }
    #[getter]
    fn get_start_time(&self) -> PyResult<String> {
        Ok(self.core.data.start_time.clone())
    }
    #[getter]
    fn get_openings(&self) -> PyResult<usize> {
        Ok(self.core.data.static_params.openings)
    }
    #[getter]
    fn get_islands(&self) -> PyResult<usize> {
        Ok(self.core.data.static_params.islands)
    }
    #[getter]
    fn get_hizi(&self) -> PyResult<usize> {
        Ok(self.core.data.static_params.hizi)
    }
    #[getter]
    fn get_cell0(&self) -> PyResult<usize> {
        Ok(self.core.data.static_params.cell0)
    }
    #[getter]
    fn get_cell1(&self) -> PyResult<usize> {
        Ok(self.core.data.static_params.cell1)
    }
    #[getter]
    fn get_cell2(&self) -> PyResult<usize> {
        Ok(self.core.data.static_params.cell2)
    }
    #[getter]
    fn get_cell3(&self) -> PyResult<usize> {
        Ok(self.core.data.static_params.cell3)
    }
    #[getter]
    fn get_cell4(&self) -> PyResult<usize> {
        Ok(self.core.data.static_params.cell4)
    }
    #[getter]
    fn get_cell5(&self) -> PyResult<usize> {
        Ok(self.core.data.static_params.cell5)
    }
    #[getter]
    fn get_cell6(&self) -> PyResult<usize> {
        Ok(self.core.data.static_params.cell6)
    }
    #[getter]
    fn get_cell7(&self) -> PyResult<usize> {
        Ok(self.core.data.static_params.cell7)
    }
    #[getter]
    fn get_cell8(&self) -> PyResult<usize> {
        Ok(self.core.data.static_params.cell8)
    }
    #[getter]
    fn get_r_time(&self) -> PyResult<f64> {
        Ok(self.core.data.dynamic_params.r_time)
    }
    #[getter]
    fn get_r_time_ms(&self) -> PyResult<u32> {
        Ok(self.core.data.dynamic_params.r_time_ms)
    }
    #[getter]
    fn get_bbbv_s(&self) -> PyResult<f64> {
        Ok(self.core.data.dynamic_params.bbbv_s)
    }
    #[getter]
    fn get_stnb(&self) -> PyResult<f64> {
        Ok(self.core.data.dynamic_params.stnb)
    }
    #[getter]
    fn get_rqp(&self) -> PyResult<f64> {
        Ok(self.core.data.dynamic_params.rqp)
    }
    #[getter]
    fn get_lefts(&self) -> PyResult<usize> {
        Ok(self.core.data.dynamic_params.lefts)
    }
    #[getter]
    fn get_rights(&self) -> PyResult<usize> {
        Ok(self.core.data.dynamic_params.rights)
    }
    #[getter]
    fn get_chordings(&self) -> PyResult<usize> {
        Ok(self.core.data.dynamic_params.chordings)
    }
    #[getter]
    fn get_clicks(&self) -> PyResult<usize> {
        Ok(self.core.data.dynamic_params.clicks)
    }
    #[getter]
    fn get_flags(&self) -> PyResult<usize> {
        Ok(self.core.data.dynamic_params.flags)
    }
    #[getter]
    fn get_ces(&self) -> PyResult<usize> {
        Ok(self.core.data.dynamic_params.ces)
    }
    #[getter]
    fn get_lefts_s(&self) -> PyResult<f64> {
        Ok(self.core.data.dynamic_params.lefts_s)
    }
    #[getter]
    fn get_rights_s(&self) -> PyResult<f64> {
        Ok(self.core.data.dynamic_params.rights_s)
    }
    #[getter]
    fn get_chordings_s(&self) -> PyResult<f64> {
        Ok(self.core.data.dynamic_params.chordings_s)
    }
    #[getter]
    fn get_clicks_s(&self) -> PyResult<f64> {
        Ok(self.core.data.dynamic_params.clicks_s)
    }
    #[getter]
    fn get_ces_s(&self) -> PyResult<f64> {
        Ok(self.core.data.dynamic_params.ces_s)
    }
    #[getter]
    fn get_ioe(&self) -> PyResult<f64> {
        Ok(self.core.data.dynamic_params.ioe)
    }
    #[getter]
    fn get_thrp(&self) -> PyResult<f64> {
        Ok(self.core.data.dynamic_params.thrp)
    }
    #[getter]
    fn get_corr(&self) -> PyResult<f64> {
        Ok(self.core.data.dynamic_params.corr)
    }
    #[getter]
    fn get_events_len(&self) -> PyResult<usize> {
        Ok(self.core.data.events.len())
    }
    pub fn events_time(&self, index: usize) -> PyResult<f64> {
        Ok(self.core.data.events[index].time)
    }
    pub fn events_mouse(&self, index: usize) -> PyResult<String> {
        Ok(self.core.data.events[index].mouse.clone())
    }
    pub fn events_x(&self, index: usize) -> PyResult<u16> {
        Ok(self.core.data.events[index].x)
    }
    pub fn events_y(&self, index: usize) -> PyResult<u16> {
        Ok(self.core.data.events[index].y)
    }
    pub fn events_useful_level(&self, index: usize) -> PyResult<u8> {
        Ok(self.core.data.events[index].useful_level)
    }
    pub fn events_prior_game_board(&self, index: usize) -> PyResult<PyGameBoard> {
        let mut t = PyGameBoard::new(self.core.data.mine_num);
        t.set_core(self.core.data.game_board_stream[self.core.data.events[index].prior_game_board_id].clone());
        Ok(t)
    }
    pub fn events_comments(&self, index: usize) -> PyResult<String> {
        Ok(self.core.data.events[index].comments.clone())
    }
    pub fn events_mouse_state(&self, index: usize) -> PyResult<usize> {
        match self.core.data.events[index].mouse_state {
            MouseState::UpUp => Ok(1),
            MouseState::UpDown => Ok(2),
            MouseState::UpDownNotFlag => Ok(3),
            MouseState::DownUp => Ok(4),
            MouseState::Chording => Ok(5),
            MouseState::ChordingNotFlag => Ok(6),
            MouseState::DownUpAfterChording => Ok(7),
            MouseState::Undefined => Ok(8),
        }
    }
    #[getter]
    pub fn get_current_event_id(&self) -> PyResult<usize> {
        Ok(self.core.data.current_event_id)
    }
    #[setter]
    pub fn set_current_event_id(&mut self, id: usize) {
        self.core.data.current_event_id = id
    }
    #[getter]
    pub fn get_game_board(&self) -> PyResult<Vec<Vec<i32>>> {
        Ok(self.core.data.get_game_board())
    }
    #[getter]
    pub fn get_game_board_poss(&mut self) -> PyResult<Vec<Vec<f64>>> {
        Ok(self.core.data.get_game_board_poss())
    }
    #[getter]
    pub fn get_mouse_state(&self) -> PyResult<usize> {
        match self.core.data.events[self.core.data.current_event_id].mouse_state {
            MouseState::UpUp => Ok(1),
            MouseState::UpDown => Ok(2),
            MouseState::UpDownNotFlag => Ok(3),
            MouseState::DownUp => Ok(4),
            MouseState::Chording => Ok(5),
            MouseState::ChordingNotFlag => Ok(6),
            MouseState::DownUpAfterChording => Ok(7),
            MouseState::Undefined => Ok(8),
        }
    }
    /// 局面状态（录像播放器的局面状态始终等于1，没有ready、win、fail的概念）
    #[getter]
    pub fn get_game_board_state(&self) -> PyResult<usize> {
        Ok(1)
    }
    /// 返回当前光标的位置，播放录像用
    #[getter]
    pub fn get_x_y(&self) -> PyResult<(u16, u16)> {
        Ok((
            self.core.data.events[self.core.data.current_event_id].x,
            self.core.data.events[self.core.data.current_event_id].y,
        ))
    }
    #[setter]
    pub fn set_time(&mut self, time: f64) {
        self.core.data.set_current_event_time(time);
    }
}

#[pyclass(name = "GameBoard")]
pub struct PyGameBoard {
    pub core: GameBoard,
}

impl PyGameBoard {
    fn set_core(&mut self, value: GameBoard) {
        self.core = value;
    }
}

#[pymethods]
impl PyGameBoard {
    #[new]
    pub fn new(mine_num: usize) -> PyGameBoard {
        let c = GameBoard::new(mine_num);
        PyGameBoard { core: c }
    }
    #[setter]
    fn set_game_board(&mut self, board: Vec<Vec<i32>>) {
        self.core.set_game_board(&board);
    }
    #[getter]
    fn get_poss(&mut self) -> PyResult<Vec<Vec<f64>>> {
        Ok(self.core.get_poss().to_vec())
    }
    #[getter]
    fn get_basic_not_mine(&mut self) -> PyResult<Vec<(usize, usize)>> {
        Ok(self.core.get_basic_not_mine().to_vec())
    }
    #[getter]
    fn get_basic_is_mine(&mut self) -> PyResult<Vec<(usize, usize)>> {
        Ok(self.core.get_basic_is_mine().to_vec())
    }
    #[getter]
    fn get_enum_not_mine(&mut self) -> PyResult<Vec<(usize, usize)>> {
        Ok(self.core.get_enum_not_mine().to_vec())
    }
    #[getter]
    fn get_enum_is_mine(&mut self) -> PyResult<Vec<(usize, usize)>> {
        Ok(self.core.get_enum_is_mine().to_vec())
    }
}
