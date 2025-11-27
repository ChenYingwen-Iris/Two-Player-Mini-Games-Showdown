# 游戏启动器音频系统

## 🎵 音频文件

### 1. 主菜单BGM - `menu_bgm.wav`
**风格**: 欢快、轻松的像素风格循环音乐  
**时长**: 8秒  
**节奏**: 120 BPM, 4/4拍  
**乐器**: 
- 方波旋律线（主旋律）
- 方波贝斯（低音律动）
- 方波和弦（背景衬托）

**音乐结构**:
```
小节1-2: C大调，欢快开场
小节3-4: G大调，律动发展  
小节5-6: Am和弦，高潮部分
小节7-8: 回到C大调，平稳收尾
```

**使用场景**:
- ✅ 主菜单界面（MENU）
- ✅ 转盘旋转界面（SPINNING）
- ✅ 等待开始界面（WAITING）
- ❌ 游戏进行中（PLAYING）
- ❌ 最终结算界面（FINAL）

**播放方式**: 无限循环

### 2. 胜利音效 - `victory.wav`
**风格**: 庆祝、欢快的胜利旋律  
**时长**: 1.2秒  
**节奏**: 140 BPM  
**乐器**:
- 方波旋律（快速上升音阶）
- 三角波和弦（柔和衬托）
- 噪音打击乐（节奏强化）

**音乐结构**:
```
0.0-0.6s: C-D-E-G-C 快速上升
0.6-1.2s: E-G-C-E-C 欢快结束
配合: 3次打击乐点缀
```

**使用场景**:
- ✅ 最终结算界面（FINAL）- 仅播放一次
- ❌ 其他所有状态

**播放方式**: 单次播放

## 🔧 技术实现

### 音频参数
```python
采样率: 44100 Hz
位深度: 16-bit
声道: 单声道 (Mono)
格式: WAV
```

### 音量控制
- **主菜单BGM**: 整体音量 0.8，各轨道音量平衡
  - 旋律: 0.25
  - 贝斯: 0.15
  - 和弦: 0.08
  
- **胜利音效**: 整体音量 0.9
  - 旋律: 0.4
  - 和弦: 0.15
  - 打击乐: 0.06

### 波形类型
1. **方波 (Square Wave)**: 像素游戏经典音色，明亮有力
2. **三角波 (Triangle Wave)**: 柔和的音色，用于和弦
3. **噪音 (Noise)**: 模拟打击乐效果

### ADSR包络
所有音符都应用了ADSR包络，使声音更自然：
```python
Attack:  0.01s  (快速起音)
Decay:   0.05s  (衰减)
Sustain: 0.7    (持续音量70%)
Release: 0.1s   (释放)
```

## 🎮 游戏中的使用

### 代码集成位置
**文件**: `game_launcher.py`

#### 1. 音频加载 (Lines 203-230)
```python
AUDIO = load_audio()
# 返回字典: {'menu_bgm': Sound对象, 'victory': Sound对象}
```

#### 2. 初始播放 (Lines 685-691)
```python
# 游戏启动时自动播放主菜单BGM
if AUDIO['menu_bgm']:
    AUDIO['menu_bgm'].play(loops=-1)  # 无限循环
```

#### 3. 游戏启动时停止 (Lines 760-764)
```python
# 进入PLAYING状态时停止BGM
if menu_bgm_playing and AUDIO['menu_bgm']:
    AUDIO['menu_bgm'].stop()
```

#### 4. 返回菜单时恢复 (Lines 776-780)
```python
# 游戏结束但还有其他游戏时，恢复BGM
if not menu_bgm_playing and AUDIO['menu_bgm']:
    AUDIO['menu_bgm'].play(loops=-1)
```

#### 5. 胜利音效播放 (Lines 944-949)
```python
# 进入FINAL状态时播放胜利音效（只播放一次）
if not victory_sound_played and AUDIO['victory']:
    AUDIO['victory'].play()
    victory_sound_played = True
```

### 状态转换与音频

```
状态流程图：

MENU (BGM循环) 
  ↓ 按SPACE
SPINNING (BGM继续)
  ↓ 转盘停止
WAITING (BGM继续)
  ↓ 按ENTER
PLAYING (停止BGM) ──┐
  ↓                 │
  ├─ 还有游戏 → MENU (恢复BGM)
  └─ 全部完成 → FINAL (播放胜利音效)
```

### 音频状态变量
```python
menu_bgm_playing: bool      # 主菜单BGM是否正在播放
victory_sound_played: bool  # 胜利音效是否已播放
```

## 📊 音频特性对比

| 特性 | 主菜单BGM | 胜利音效 |
|------|----------|---------|
| 时长 | 8秒 | 1.2秒 |
| 循环 | ✅ 无限 | ❌ 单次 |
| BPM | 120 | 140 |
| 音轨数 | 3（旋律+贝斯+和弦） | 3（旋律+和弦+打击） |
| 主波形 | 方波 | 方波+三角波 |
| 音量 | 0.8 | 0.9 |
| 情绪 | 轻松欢快 | 兴奋庆祝 |

## 🎨 音乐设计理念

### 主菜单BGM
**目标**: 营造轻松、友好的氛围，让玩家感到舒适  

**设计要点**:
1. **简单旋律**: 易记、不喧宾夺主
2. **循环流畅**: 8秒循环无缝衔接
3. **节奏稳定**: 120 BPM适中节奏
4. **和声简洁**: C-G-Am-G 经典进行

**情绪曲线**:
```
起 ━━━━━━ 欢快开场
承 ━━━━━━ 律动发展
转 ━━━━━━ 高潮部分
合 ━━━━━━ 平稳收尾 → 循环
```

### 胜利音效
**目标**: 提供即时的成就感和庆祝氛围

**设计要点**:
1. **快速上升**: 音阶快速向上，象征胜利
2. **明亮音色**: 方波+三角波组合，欢快响亮
3. **打击强化**: 3次打击乐增强节奏感
4. **短促有力**: 1.2秒快速结束，不拖沓

**情绪曲线**:
```
0.0s ━ 开始兴奋 ⬆️
0.3s ━ 快速攀升 ⬆️⬆️
0.6s ━ 达到顶峰 🎉
1.2s ━ 满足结束 ✨
```

## 🛠️ 生成工具

### 音频生成脚本
**文件**: `generate_launcher_audio.py`

**使用方法**:
```bash
python3 generate_launcher_audio.py
```

**输出**:
```
launcher_audio/
├── menu_bgm.wav    (主菜单BGM)
└── victory.wav     (胜利音效)
```

**依赖**:
- numpy（音频数据处理）
- wave（WAV文件写入）

### 自定义音乐参数

如需调整音乐，可修改以下参数：

#### BPM（节奏速度）
```python
# 在 generate_menu_bgm() 中
bpm = 120  # 可调整为 100-140
```

#### 音量
```python
# 旋律音量
generate_note(..., volume=0.25)  # 可调整 0.1-0.4

# 贝斯音量
generate_note(..., volume=0.15)  # 可调整 0.1-0.3

# 和弦音量
generate_chord(..., volume=0.08)  # 可调整 0.05-0.15
```

#### 旋律音符
```python
# 修改 melody 列表中的音符
melody = [
    ('C5', 0.5),  # (音符, 时值)
    ('E5', 0.5),
    # ... 添加或修改音符
]
```

## 🐛 故障排除

### 问题1: 音频文件未找到
**症状**: 控制台显示 "⚠ 未找到主菜单BGM文件"

**解决**:
```bash
# 1. 确认音频文件存在
ls -la launcher_audio/

# 2. 重新生成音频
python3 generate_launcher_audio.py

# 3. 检查文件权限
chmod 644 launcher_audio/*.wav
```

### 问题2: 音频不播放
**症状**: 无报错但听不到声音

**解决**:
```python
# 1. 检查系统音量
# 2. 检查pygame.mixer初始化
pygame.mixer.init()

# 3. 测试播放
sound = pygame.mixer.Sound('launcher_audio/menu_bgm.wav')
sound.play()
```

### 问题3: 音频卡顿
**症状**: 播放时有断断续续

**解决**:
```python
# 增加pygame mixer缓冲区
pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
```

### 问题4: 循环有间隙
**症状**: BGM循环时有明显停顿

**解决**: 音频文件已包含淡入淡出，循环是无缝的。如仍有问题：
```python
# 使用pygame.mixer.music而非Sound
pygame.mixer.music.load('launcher_audio/menu_bgm.wav')
pygame.mixer.music.play(loops=-1)
```

## ✅ 测试清单

- [x] 主菜单BGM生成成功
- [x] 胜利音效生成成功
- [x] 游戏启动时自动播放BGM
- [x] 转盘界面BGM持续播放
- [x] 等待界面BGM持续播放
- [x] 进入游戏时BGM停止
- [x] 返回菜单时BGM恢复
- [x] 最终界面BGM停止
- [x] 最终界面播放胜利音效
- [x] 胜利音效只播放一次
- [x] 音频音量适中不刺耳
- [x] BGM循环无缝衔接

## 🎯 用户体验

### Before (无音频)
```
❌ 界面安静无声
❌ 缺少氛围感
❌ 胜利无庆祝感
❌ 游戏感不足
```

### After (有音频)
```
✅ 欢快的背景音乐
✅ 沉浸式游戏体验
✅ 胜利庆祝音效
✅ 专业游戏质感
✅ 像素风格统一
```

## 🚀 未来改进

### 可能的增强功能
1. **音量控制**: 添加用户可调节的音量滑块
2. **音乐切换**: 提供多首BGM供选择
3. **音效扩展**: 添加按键音、选择音
4. **动态音乐**: 根据游戏进度改变BGM
5. **3D音效**: 使用pygame.mixer.Channel实现立体声

### 音效扩展建议
```python
launcher_audio/
├── menu_bgm.wav      ✓ 已实现
├── victory.wav       ✓ 已实现
├── button_click.wav  (按键音)
├── spin_start.wav    (开始转盘)
├── game_select.wav   (选中游戏)
└── countdown.wav     (倒计时音)
```

---

**创建日期**: 2025年11月27日  
**音频格式**: WAV 44.1kHz 16-bit Mono  
**总大小**: ~1.5 MB  
**状态**: ✅ 已完成并集成
