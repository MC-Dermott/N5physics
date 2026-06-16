# Background video links shown to students before they practise each topic.
# All videos are from The Physics Academy (@thephysicsacad) on YouTube.
#
# Key:   (topic, question_type)  — matches the strings in question_factory.py
# Value: list of {"title": str, "url": str}
#
# For Heat sub-types (Specific Heat Capacity, Specific Latent Heat, etc.)
# the key is ("Properties", "Heat") and applies to all sub-types.

BACKGROUND_VIDEOS = {
    ("Dynamics", "Speed, Distance & Time"): [
        {"title": "Instantaneous Speed | THEORY", "url": "https://www.youtube.com/watch?v=Uc628iL6TLw"},
        {"title": "Average Speed | WORKED EXAMPLES", "url": "https://www.youtube.com/watch?v=DS6ZlqtobHo"},
    ],
    ("Dynamics", "Acceleration"): [
        {"title": "Acceleration & Deceleration | THEORY", "url": "https://www.youtube.com/watch?v=BOvBx1WFWjE"},
        {"title": "Acceleration due to Gravity | THEORY", "url": "https://www.youtube.com/watch?v=NFyV9d4B3Zg"},
    ],
    ("Dynamics", "Forces"): [
        {"title": "Newton's Second Law | THEORY", "url": "https://www.youtube.com/watch?v=B80DnIvTfOo"},
        {"title": "Free-fall & Terminal Velocity | THEORY", "url": "https://www.youtube.com/watch?v=30IZHHCxobU"},
    ],
    ("Dynamics", "Weight"): [
        {"title": "Dynamics — full playlist", "url": "https://www.youtube.com/playlist?list=PL4ViYiFUc7GQZBLHieq0dX_gLrc-Dcdtf"},
    ],
    ("Dynamics", "Energy"): [
        {"title": "Kinetic Energy | THEORY", "url": "https://www.youtube.com/watch?v=ri5Jk1uk3Gg"},
        {"title": "Gravitational Potential Energy | THEORY", "url": "https://www.youtube.com/watch?v=U5qnwN-HEw8"},
        {"title": "Kinetic Energy | WORKED EXAMPLES", "url": "https://www.youtube.com/watch?v=8Z7gG62o6FU"},
    ],
    ("Dynamics", "Projectile Motion"): [
        {"title": "Horizontal & Vertical Motion of a Projectile | THEORY", "url": "https://www.youtube.com/watch?v=twWxLEdlD_M"},
        {"title": "Time of Flight of a Projectile | THEORY", "url": "https://www.youtube.com/watch?v=EROqhX987YE"},
        {"title": "Projectile Motion | WORKED EXAMPLES", "url": "https://www.youtube.com/watch?v=rGrZBxk5dQc"},
    ],
    ("Dynamics", "Vectors"): [
        {"title": "Vector & Scalar Quantities | THEORY", "url": "https://www.youtube.com/watch?v=-YokQBWbC-8"},
        {"title": "Vector Addition & Resultant Vectors | THEORY", "url": "https://www.youtube.com/watch?v=_6jS_byd79Y"},
        {"title": "Calculation Method (Resultant Vectors) | THEORY", "url": "https://www.youtube.com/watch?v=oONevD8dlAs"},
    ],
    ("Electricity", "Current"): [
        {"title": "Electrical Current | THEORY", "url": "https://www.youtube.com/watch?v=5Yxrj5IdXtE"},
    ],
    ("Electricity", "Ohm's Law"): [
        {"title": "Ohm's Law | THEORY", "url": "https://www.youtube.com/watch?v=IPuAW1qddaw"},
        {"title": "Ohm's Law | WORKED EXAMPLES", "url": "https://www.youtube.com/watch?v=-xJgFbBOcOo"},
    ],
    ("Electricity", "Resistors"): [
        {"title": "Resistors in Series | THEORY", "url": "https://www.youtube.com/watch?v=y8AxMbmYx_U"},
        {"title": "Electricity — full playlist", "url": "https://www.youtube.com/playlist?list=PL4ViYiFUc7GTFOeKyg3-JJCaNEOoeOaOB"},
    ],
    ("Electricity", "Electrical Power"): [
        {"title": "Electrical Power | THEORY", "url": "https://www.youtube.com/watch?v=ga8TSm50XI0"},
        {"title": "Power Relationships | THEORY", "url": "https://www.youtube.com/watch?v=wh83Fipq-1s"},
        {"title": "Power Relationships | WORKED EXAMPLES", "url": "https://www.youtube.com/watch?v=4KNtwdVPuKE"},
    ],
    ("Electricity", "Potential Divider"): [
        {"title": "Potential Divider Circuits | THEORY", "url": "https://www.youtube.com/watch?v=bTexl2XhIQk"},
        {"title": "Potential Divider Circuits | WORKED EXAMPLES", "url": "https://www.youtube.com/watch?v=DQlOzNjlEoA"},
    ],
    ("Electricity", "Circuits"): [
        {"title": "Electricity — full playlist", "url": "https://www.youtube.com/playlist?list=PL4ViYiFUc7GTFOeKyg3-JJCaNEOoeOaOB"},
    ],
    ("Radiation", "Dose"): [
        {"title": "Absorbed Dose | THEORY", "url": "https://www.youtube.com/watch?v=odPfhQ8HumM"},
        {"title": "Equivalent Dose | THEORY", "url": "https://www.youtube.com/watch?v=pFLMvt68fCI"},
        {"title": "Equivalent Dose Rate | THEORY", "url": "https://www.youtube.com/watch?v=xuYmUm376kw"},
        {"title": "Absorbed Dose | WORKED EXAMPLES", "url": "https://www.youtube.com/watch?v=M6-Y2kQBmUg"},
    ],
    ("Radiation", "Half-Life"): [
        {"title": "Half-Life | THEORY", "url": "https://www.youtube.com/watch?v=mtHcljRgjto"},
    ],
    ("Radiation", "Activity"): [
        {"title": "Activity | THEORY", "url": "https://www.youtube.com/watch?v=hn5ckiFIwJo"},
    ],
    ("Waves", "Wave Speed"): [
        {"title": "Wave Speed | THEORY", "url": "https://www.youtube.com/watch?v=P43Aa0sP510"},
    ],
    ("Waves", "Period & Frequency"): [
        {"title": "Wave Frequency & Period | THEORY", "url": "https://www.youtube.com/watch?v=HJLLq-Hcqks"},
        {"title": "Wave Frequency & Period | WORKED EXAMPLES", "url": "https://www.youtube.com/watch?v=0C21fvjVKPE"},
    ],
    ("Waves", "Waves Combined"): [
        {"title": "Waves — full playlist", "url": "https://www.youtube.com/playlist?list=PL4ViYiFUc7GTctCeEsnX_Y30IoB1DiP8i"},
    ],
    ("Properties", "Pressure"): [
        {"title": "Pressure | THEORY", "url": "https://www.youtube.com/watch?v=pVw13haCHBw"},
    ],
    ("Properties", "Gas Laws"): [
        {"title": "Boyle's Law | WORKED EXAMPLES", "url": "https://www.youtube.com/watch?v=zsmg1VY-gsI"},
    ],
    ("Properties", "Heat"): [
        {"title": "Specific Heat Capacity | THEORY", "url": "https://www.youtube.com/watch?v=z1gS1iI65nw"},
        {"title": "Specific Latent Heat | THEORY", "url": "https://www.youtube.com/watch?v=pku9L5_3bCk"},
        {"title": "Specific Latent Heat | WORKED EXAMPLES", "url": "https://www.youtube.com/watch?v=9xWho8hsg6Q"},
    ],
}


def get_background_videos(topic, question_type):
    return BACKGROUND_VIDEOS.get((topic, question_type), [])
