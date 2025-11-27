"""
生成游戏启动器的音频文件
1. 主界面背景音乐 - 欢快、轻松的像素风格循环音乐
2. 胜利音效 - 庆祝、欢快的胜利旋律
"""
import numpy as np
import wave
import struct
import os

# 音频参数
SAMPLE_RATE = 44100
BIT_DEPTH = np.int16

def generate_note(frequency, duration, sample_rate=44100, wave_type='square', volume=0.3):
    """
    生成音符
    wave_type: 'square'(方波), 'sine'(正弦波), 'triangle'(三角波), 'sawtooth'(锯齿波)
    """
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    if wave_type == 'square':
        wave = np.sign(np.sin(2 * np.pi * frequency * t))
    elif wave_type == 'sine':
        wave = np.sin(2 * np.pi * frequency * t)
    elif wave_type == 'triangle':
        wave = 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1
    elif wave_type == 'sawtooth':
        wave = 2 * (t * frequency - np.floor(t * frequency + 0.5))
    else:
        wave = np.sin(2 * np.pi * frequency * t)
    
    # ADSR包络 (Attack, Decay, Sustain, Release)
    envelope = np.ones_like(t)
    attack_time = 0.01
    decay_time = 0.05
    release_time = 0.1
    sustain_level = 0.7
    
    attack_samples = int(attack_time * sample_rate)
    decay_samples = int(decay_time * sample_rate)
    release_samples = int(release_time * sample_rate)
    
    if len(t) > attack_samples:
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    if len(t) > attack_samples + decay_samples:
        envelope[attack_samples:attack_samples + decay_samples] = np.linspace(1, sustain_level, decay_samples)
        envelope[attack_samples + decay_samples:-release_samples] = sustain_level
    if len(t) > release_samples:
        envelope[-release_samples:] = np.linspace(sustain_level, 0, release_samples)
    
    return wave * envelope * volume

def note_to_freq(note):
    """音符转频率 (A4 = 440Hz)"""
    notes = {
        'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23, 'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
        'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'F5': 698.46, 'G5': 783.99, 'A5': 880.00, 'B5': 987.77,
        'C6': 1046.50, 'D6': 1174.66, 'E6': 1318.51, 'F6': 1396.91, 'G6': 1567.98,
        'C3': 130.81, 'D3': 146.83, 'E3': 164.81, 'F3': 174.61, 'G3': 196.00, 'A3': 220.00, 'B3': 246.94,
        'REST': 0
    }
    return notes.get(note, 440)

def generate_chord(notes, duration, sample_rate=44100, wave_type='square', volume=0.2):
    """生成和弦"""
    chord = np.zeros(int(sample_rate * duration))
    for note in notes:
        freq = note_to_freq(note)
        if freq > 0:
            chord += generate_note(freq, duration, sample_rate, wave_type, volume)
    return chord / len(notes)

def generate_menu_bgm():
    """
    生成主菜单背景音乐
    风格：欢快、轻松、像素风格
    节奏：4/4拍，约120 BPM
    """
    print("🎵 生成主菜单背景音乐...")
    
    bpm = 120
    beat_duration = 60.0 / bpm  # 一拍的时长
    
    # 主旋律 - 欢快的旋律线
    melody = [
        # 第1-2小节：开场
        ('C5', 0.5), ('E5', 0.5), ('G5', 0.5), ('E5', 0.5),
        ('C5', 0.5), ('E5', 0.5), ('G5', 1.0),
        
        # 第3-4小节：发展
        ('D5', 0.5), ('F5', 0.5), ('A5', 0.5), ('F5', 0.5),
        ('D5', 0.5), ('F5', 0.5), ('A5', 1.0),
        
        # 第5-6小节：高潮
        ('E5', 0.5), ('G5', 0.5), ('C6', 0.5), ('G5', 0.5),
        ('E5', 0.5), ('G5', 0.5), ('C6', 1.0),
        
        # 第7-8小节：回归
        ('G5', 0.5), ('E5', 0.5), ('C5', 0.5), ('E5', 0.5),
        ('G5', 1.0), ('C5', 1.0),
    ]
    
    # 低音贝斯 - 简单的根音律动
    bass = [
        # 重复4次
        ('C3', 1.0), ('C3', 1.0), ('C3', 1.0), ('C3', 1.0),
        ('G3', 1.0), ('G3', 1.0), ('G3', 1.0), ('G3', 1.0),
        ('A3', 1.0), ('A3', 1.0), ('A3', 1.0), ('A3', 1.0),
        ('G3', 1.0), ('G3', 1.0), ('C3', 1.0), ('C3', 1.0),
    ]
    
    # 和弦伴奏
    chords = [
        # C大调进行
        (['C4', 'E4', 'G4'], 2.0),
        (['C4', 'E4', 'G4'], 2.0),
        (['G3', 'B3', 'D4'], 2.0),
        (['G3', 'B3', 'D4'], 2.0),
        (['A3', 'C4', 'E4'], 2.0),
        (['A3', 'C4', 'E4'], 2.0),
        (['G3', 'B3', 'D4'], 2.0),
        (['C4', 'E4', 'G4'], 2.0),
    ]
    
    # 生成旋律轨道
    melody_track = np.array([])
    for note, duration in melody:
        freq = note_to_freq(note)
        if freq > 0:
            tone = generate_note(freq, duration * beat_duration, wave_type='square', volume=0.25)
        else:
            tone = np.zeros(int(SAMPLE_RATE * duration * beat_duration))
        melody_track = np.concatenate([melody_track, tone])
    
    # 生成贝斯轨道
    bass_track = np.array([])
    for note, duration in bass:
        freq = note_to_freq(note)
        if freq > 0:
            tone = generate_note(freq, duration * beat_duration, wave_type='square', volume=0.15)
        else:
            tone = np.zeros(int(SAMPLE_RATE * duration * beat_duration))
        bass_track = np.concatenate([bass_track, tone])
    
    # 生成和弦轨道
    chord_track = np.array([])
    for notes, duration in chords:
        chord = generate_chord(notes, duration * beat_duration, wave_type='square', volume=0.08)
        chord_track = np.concatenate([chord_track, chord])
    
    # 混合所有轨道
    max_len = max(len(melody_track), len(bass_track), len(chord_track))
    melody_track = np.pad(melody_track, (0, max_len - len(melody_track)))
    bass_track = np.pad(bass_track, (0, max_len - len(bass_track)))
    chord_track = np.pad(chord_track, (0, max_len - len(chord_track)))
    
    audio = melody_track + bass_track + chord_track
    
    # 归一化
    audio = audio / np.max(np.abs(audio)) * 0.8
    
    # 淡入淡出
    fade_duration = int(SAMPLE_RATE * 0.5)
    audio[:fade_duration] *= np.linspace(0, 1, fade_duration)
    audio[-fade_duration:] *= np.linspace(1, 0, fade_duration)
    
    return audio

def generate_victory_sound():
    """
    生成胜利音效
    风格：欢快、庆祝、短促有力
    """
    print("🏆 生成胜利音效...")
    
    bpm = 140
    beat_duration = 60.0 / bpm
    
    # 胜利旋律 - 上升的音阶 + 欢快结尾
    victory_melody = [
        # 快速上升
        ('C5', 0.15), ('D5', 0.15), ('E5', 0.15), ('G5', 0.15),
        ('C6', 0.3), ('REST', 0.1),
        
        # 欢快结束
        ('E6', 0.2), ('G6', 0.2), ('C6', 0.4),
        ('E6', 0.2), ('C6', 0.6),
    ]
    
    # 和弦衬托
    victory_chords = [
        (['C4', 'E4', 'G4'], 0.6),
        (['C5', 'E5', 'G5'], 0.6),
        (['C5', 'E5', 'G5', 'C6'], 1.2),
    ]
    
    # 生成旋律
    melody_track = np.array([])
    for note, duration in victory_melody:
        freq = note_to_freq(note)
        if freq > 0:
            tone = generate_note(freq, duration * beat_duration, wave_type='square', volume=0.4)
        else:
            tone = np.zeros(int(SAMPLE_RATE * duration * beat_duration))
        melody_track = np.concatenate([melody_track, tone])
    
    # 生成和弦
    chord_track = np.array([])
    for notes, duration in victory_chords:
        chord = generate_chord(notes, duration * beat_duration, wave_type='triangle', volume=0.15)
        chord_track = np.concatenate([chord_track, chord])
    
    # 添加打击乐效果（使用噪音模拟）
    percussion = np.array([])
    for i in range(3):  # 3次打击
        hit = np.random.randn(int(SAMPLE_RATE * 0.05)) * 0.2
        silence = np.zeros(int(SAMPLE_RATE * 0.35))
        percussion = np.concatenate([percussion, hit, silence])
    
    # 混合轨道
    max_len = max(len(melody_track), len(chord_track), len(percussion))
    melody_track = np.pad(melody_track, (0, max_len - len(melody_track)))
    chord_track = np.pad(chord_track, (0, max_len - len(chord_track)))
    percussion = np.pad(percussion, (0, max_len - len(percussion)))
    
    audio = melody_track + chord_track + percussion * 0.3
    
    # 归一化
    audio = audio / np.max(np.abs(audio)) * 0.9
    
    # 淡出
    fade_duration = int(SAMPLE_RATE * 0.3)
    audio[-fade_duration:] *= np.linspace(1, 0, fade_duration)
    
    return audio

def save_audio(audio, filename):
    """保存音频文件"""
    # 转换为16位整数
    audio_int = np.int16(audio * 32767)
    
    # 使用wave模块保存
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # 单声道
        wav_file.setsampwidth(2)  # 16位 = 2字节
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(audio_int.tobytes())
    
    print(f"✓ 保存文件: {filename}")

def main():
    """生成所有音频文件"""
    print("=" * 60)
    print("🎮 Two Player Mini Games Showdown - 音频生成器")
    print("=" * 60)
    
    # 创建音频目录
    audio_dir = "launcher_audio"
    os.makedirs(audio_dir, exist_ok=True)
    print(f"\n📁 音频保存目录: {audio_dir}/\n")
    
    # 生成主菜单BGM
    menu_bgm = generate_menu_bgm()
    save_audio(menu_bgm, os.path.join(audio_dir, "menu_bgm.wav"))
    print(f"   时长: {len(menu_bgm) / SAMPLE_RATE:.2f} 秒")
    print(f"   用途: 主界面背景音乐（循环播放）\n")
    
    # 生成胜利音效
    victory_sound = generate_victory_sound()
    save_audio(victory_sound, os.path.join(audio_dir, "victory.wav"))
    print(f"   时长: {len(victory_sound) / SAMPLE_RATE:.2f} 秒")
    print(f"   用途: 游戏结束胜利音效\n")
    
    print("=" * 60)
    print("✅ 所有音频文件生成完成！")
    print("=" * 60)
    print("\n📝 使用说明:")
    print("1. menu_bgm.wav - 在主界面、转盘、等待界面循环播放")
    print("2. victory.wav - 在最终结算界面播放一次")
    print("\n💡 提示:")
    print("- 音频文件为 44.1kHz, 16-bit WAV 格式")
    print("- 像素风格的方波和三角波音色")
    print("- 音量已优化，不会过响")
    print()

if __name__ == "__main__":
    main()
