/**
 * 五子棋游戏JavaScript逻辑
 * 实现游戏规则、棋盘渲染和用户交互
 */

// 游戏状态变量
let board = []; // 棋盘状态
let currentPlayer = 'black'; // 当前玩家 ('black' 或 'white')
let gameOver = false; // 游戏是否结束
let moveHistory = []; // 落子历史，用于悔棋功能

// 棋盘配置
const BOARD_SIZE = 15; // 15x15棋盘
const CELL_SIZE = 30; // 每个格子的大小（像素）

// DOM元素引用
const gameBoard = document.getElementById('game-board');
const currentPlayerSpan = document.getElementById('current-player');
const winnerMessage = document.getElementById('winner-message');
const restartBtn = document.getElementById('restart-btn');
const undoBtn = document.getElementById('undo-btn');

/**
 * 初始化游戏
 */
function initGame() {
    // 初始化棋盘状态
    board = Array(BOARD_SIZE).fill().map(() => Array(BOARD_SIZE).fill(null));
    
    // 重置游戏状态
    currentPlayer = 'black';
    gameOver = false;
    moveHistory = [];
    
    // 更新UI
    currentPlayerSpan.textContent = '黑棋';
    currentPlayerSpan.style.color = '#000';
    winnerMessage.textContent = '';
    winnerMessage.style.color = '#e74c3c';
    
    // 渲染棋盘
    renderBoard();
    
    // 绑定事件监听器
    bindEventListeners();
    
    // 添加初始化提示
    showTemporaryMessage("游戏开始！黑棋先手。");
}

/**
 * 渲染棋盘
 */
function renderBoard() {
    // 清空棋盘
    gameBoard.innerHTML = '';
    
    // 设置棋盘大小
    gameBoard.style.width = `${BOARD_SIZE * CELL_SIZE + 20}px`;
    gameBoard.style.height = `${BOARD_SIZE * CELL_SIZE + 20}px`;
    gameBoard.style.position = 'relative';
    
    // 创建棋盘格子
    for (let row = 0; row < BOARD_SIZE; row++) {
        for (let col = 0; col < BOARD_SIZE; col++) {
            const cell = document.createElement('div');
            cell.style.position = 'absolute';
            cell.style.width = `${CELL_SIZE}px`;
            cell.style.height = `${CELL_SIZE}px`;
            cell.style.left = `${col * CELL_SIZE + 10}px`;
            cell.style.top = `${row * CELL_SIZE + 10}px`;
            cell.style.cursor = 'pointer';
            cell.dataset.row = row;
            cell.dataset.col = col;
            
            // 添加悬停效果
            cell.addEventListener('mouseenter', function() {
                if (!gameOver && !board[row][col] && this.childElementCount === 0) {
                    const hoverPiece = document.createElement('div');
                    hoverPiece.className = `piece ${currentPlayer} hover`;
                    hoverPiece.style.opacity = '0.7';
                    this.appendChild(hoverPiece);
                }
            });
            
            cell.addEventListener('mouseleave', function() {
                if (this.firstChild && this.firstChild.classList.contains('hover')) {
                    this.removeChild(this.firstChild);
                }
            });
            
            // 如果该位置有棋子，则渲染棋子
            if (board[row][col]) {
                const piece = document.createElement('div');
                piece.className = `piece ${board[row][col]}`;
                piece.style.left = `${col * CELL_SIZE + 11}px`;
                piece.style.top = `${row * CELL_SIZE + 11}px`;
                gameBoard.appendChild(piece);
            }
            
            gameBoard.appendChild(cell);
        }
    }
}

/**
 * 绑定事件监听器
 */
function bindEventListeners() {
    // 点击棋盘落子
    gameBoard.addEventListener('click', handleBoardClick);
    
    // 重新开始按钮
    restartBtn.addEventListener('click', function() {
        if (confirm("确定要重新开始游戏吗？")) {
            initGame();
        }
    });
    
    // 悔棋按钮
    undoBtn.addEventListener('click', function() {
        if (moveHistory.length > 0 && confirm("确定要悔棋吗？")) {
            undoMove();
        }
    });
}

/**
 * 处理棋盘点击事件
 * @param {Event} event - 点击事件
 */
function handleBoardClick(event) {
    // 如果游戏已结束，不处理点击
    if (gameOver) return;
    
    // 获取点击位置
    let target = event.target;
    
    // 如果点击的是棋子，需要找到对应的空位
    if (target.classList.contains('piece')) {
        target = target.parentElement;
    }
    
    // 获取行列坐标
    const row = parseInt(target.dataset.row);
    const col = parseInt(target.dataset.col);
    
    // 检查坐标有效性
    if (isNaN(row) || isNaN(col)) return;
    
    // 检查该位置是否为空
    if (board[row][col] !== null) return;
    
    // 播放落子音效
    playMoveSound();
    
    // 落子
    makeMove(row, col);
}

/**
 * 落子
 * @param {number} row - 行坐标
 * @param {number} col - 列坐标
 */
function makeMove(row, col) {
    // 更新棋盘状态
    board[row][col] = currentPlayer;
    
    // 记录落子历史
    moveHistory.push({ row, col, player: currentPlayer });
    
    // 检查是否获胜
    if (checkWin(row, col)) {
        // 游戏结束，显示获胜信息
        gameOver = true;
        const winner = currentPlayer === 'black' ? '黑棋' : '白棋';
        winnerMessage.textContent = `${winner}获胜！`;
        winnerMessage.style.color = currentPlayer === 'black' ? '#000' : '#fff';
        winnerMessage.style.textShadow = currentPlayer === 'black' ? 
            '1px 1px 2px #fff' : '1px 1px 2px #000';
        
        // 播放胜利音效
        playWinSound();
        
        // 显示获胜提示
        showTemporaryMessage(`恭喜！${winner}获胜！`);
        return;
    }
    
    // 检查是否平局（棋盘已满）
    if (moveHistory.length === BOARD_SIZE * BOARD_SIZE) {
        gameOver = true;
        winnerMessage.textContent = '平局！';
        
        // 显示平局提示
        showTemporaryMessage("平局！");
        return;
    }
    
    // 切换玩家
    currentPlayer = currentPlayer === 'black' ? 'white' : 'black';
    currentPlayerSpan.textContent = currentPlayer === 'black' ? '黑棋' : '白棋';
    currentPlayerSpan.style.color = currentPlayer === 'black' ? '#000' : '#fff';
    currentPlayerSpan.style.textShadow = currentPlayer === 'black' ? 
        '1px 1px 2px #fff' : '1px 1px 2px #000';
    
    // 重新渲染棋盘
    renderBoard();
    
    // 显示玩家切换提示
    showTemporaryMessage(`${currentPlayer === 'black' ? '黑棋' : '白棋'}落子`);
}

/**
 * 检查是否获胜
 * @param {number} row - 最后落子的行坐标
 * @param {number} col - 最后落子的列坐标
 * @returns {boolean} 是否获胜
 */
function checkWin(row, col) {
    const player = board[row][col];
    if (!player) return false;
    
    // 检查四个方向：水平、垂直、主对角线、副对角线
    const directions = [
        [0, 1],   // 水平
        [1, 0],   // 垂直
        [1, 1],   // 主对角线
        [1, -1]   // 副对角线
    ];
    
    // 检查每个方向
    for (const [dx, dy] of directions) {
        let count = 1; // 包含当前棋子
        
        // 向正方向检查
        for (let i = 1; i < 5; i++) {
            const r = row + dx * i;
            const c = col + dy * i;
            if (r >= 0 && r < BOARD_SIZE && c >= 0 && c < BOARD_SIZE && board[r][c] === player) {
                count++;
            } else {
                break;
            }
        }
        
        // 向反方向检查
        for (let i = 1; i < 5; i++) {
            const r = row - dx * i;
            const c = col - dy * i;
            if (r >= 0 && r < BOARD_SIZE && c >= 0 && c < BOARD_SIZE && board[r][c] === player) {
                count++;
            } else {
                break;
            }
        }
        
        // 如果连成五子，则获胜
        if (count >= 5) {
            return true;
        }
    }
    
    return false;
}

/**
 * 悔棋功能
 */
function undoMove() {
    // 如果游戏已结束或没有落子历史，不能悔棋
    if (gameOver || moveHistory.length === 0) {
        showTemporaryMessage("无法悔棋");
        return;
    }
    
    // 获取最后一步棋
    const lastMove = moveHistory.pop();
    
    // 清空该位置的棋子
    board[lastMove.row][lastMove.col] = null;
    
    // 如果还有历史记录，恢复到上一个玩家
    if (moveHistory.length > 0) {
        const prevMove = moveHistory[moveHistory.length - 1];
        currentPlayer = prevMove.player === 'black' ? 'white' : 'black';
    } else {
        // 如果没有历史记录，恢复到初始玩家
        currentPlayer = 'black';
    }
    
    // 更新UI
    currentPlayerSpan.textContent = currentPlayer === 'black' ? '黑棋' : '白棋';
    currentPlayerSpan.style.color = currentPlayer === 'black' ? '#000' : '#fff';
    winnerMessage.textContent = '';
    gameOver = false;
    
    // 重新渲染棋盘
    renderBoard();
    
    // 显示悔棋提示
    showTemporaryMessage("悔棋成功");
}

/**
 * 显示临时消息
 * @param {string} message - 要显示的消息
 */
function showTemporaryMessage(message) {
    // 创建临时消息元素
    const tempMessage = document.createElement('div');
    tempMessage.textContent = message;
    tempMessage.style.position = 'fixed';
    tempMessage.style.top = '20px';
    tempMessage.style.left = '50%';
    tempMessage.style.transform = 'translateX(-50%)';
    tempMessage.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
    tempMessage.style.color = 'white';
    tempMessage.style.padding = '10px 20px';
    tempMessage.style.borderRadius = '5px';
    tempMessage.style.zIndex = '1000';
    tempMessage.style.transition = 'opacity 0.5s';
    
    // 添加到页面
    document.body.appendChild(tempMessage);
    
    // 3秒后淡出并移除
    setTimeout(() => {
        tempMessage.style.opacity = '0';
        setTimeout(() => {
            if (tempMessage.parentNode) {
                tempMessage.parentNode.removeChild(tempMessage);
            }
        }, 500);
    }, 3000);
}

/**
 * 播放落子音效
 */
function playMoveSound() {
    // 创建音频上下文
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.type = 'sine';
        oscillator.frequency.value = 440;
        gainNode.gain.value = 0.1;
        
        oscillator.start();
        setTimeout(() => {
            oscillator.stop();
        }, 100);
    } catch (e) {
        // 静默失败，不支持音频API的浏览器不会报错
    }
}

/**
 * 播放胜利音效
 */
function playWinSound() {
    // 创建音频上下文
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.type = 'sine';
        oscillator.frequency.value = 523.25; // C5
        gainNode.gain.value = 0.1;
        
        oscillator.start();
        
        // 播放胜利音调序列
        setTimeout(() => {
            oscillator.frequency.value = 659.25; // E5
        }, 150);
        
        setTimeout(() => {
            oscillator.frequency.value = 783.99; // G5
        }, 300);
        
        setTimeout(() => {
            oscillator.stop();
        }, 500);
    } catch (e) {
        // 静默失败
    }
}

// 页面加载完成后初始化游戏
document.addEventListener('DOMContentLoaded', initGame);