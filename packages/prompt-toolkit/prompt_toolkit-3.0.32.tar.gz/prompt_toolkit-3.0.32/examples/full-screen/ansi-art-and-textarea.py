#!/usr/bin/env python

from prompt_toolkit.application import Application
from prompt_toolkit.formatted_text import ANSI, HTML
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import (
    FormattedTextControl,
    HSplit,
    Layout,
    VSplit,
    Window,
    WindowAlign,
)
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.widgets import Dialog, Label, TextArea


def main():
    # Key bindings.
    kb = KeyBindings()

    @kb.add("c-c")
    def _(event):
        "Quit when control-c is pressed."
        event.app.exit()

    text_area = TextArea(text="You can type here...")
    dialog_body = HSplit(
        [
            Label(
                HTML("Press <reverse>control-c</reverse> to quit."),
                align=WindowAlign.CENTER,
            ),
            VSplit(
                [
                    Label(PROMPT_TOOLKIT_LOGO, align=WindowAlign.CENTER),
                    text_area,
                ],
            ),
        ]
    )

    application = Application(
        layout=Layout(
            container=Dialog(
                title="ANSI Art demo - Art on the left, text area on the right",
                body=dialog_body,
                with_background=True,
            ),
            focused_element=text_area,
        ),
        full_screen=True,
        mouse_support=True,
        key_bindings=kb,
    )
    application.run()


PROMPT_TOOLKIT_LOGO = ANSI(
    """
\x1b[48;2;0;0;0m                                                  \x1b[m
\x1b[48;2;0;0;0m         \x1b[48;2;0;249;0m\x1b[38;2;0;0;0m▀\x1b[48;2;0;209;0m▀\x1b[48;2;0;207;0m\x1b[38;2;6;34;6m▀\x1b[48;2;0;66;0m\x1b[38;2;30;171;30m▀\x1b[48;2;0;169;0m\x1b[38;2;51;35;51m▀\x1b[48;2;0;248;0m\x1b[38;2;49;194;49m▀\x1b[48;2;0;111;0m\x1b[38;2;25;57;25m▀\x1b[48;2;140;195;140m\x1b[38;2;3;17;3m▀\x1b[48;2;30;171;30m\x1b[38;2;0;0;0m▀\x1b[48;2;0;0;0m                                \x1b[m
\x1b[48;2;0;0;0m \x1b[48;2;77;127;78m\x1b[38;2;118;227;108m▀\x1b[48;2;216;1;13m\x1b[38;2;49;221;57m▀\x1b[48;2;26;142;76m\x1b[38;2;108;146;165m▀\x1b[48;2;26;142;90m\x1b[38;2;209;197;114m▀▀\x1b[38;2;209;146;114m▀\x1b[48;2;26;128;90m\x1b[38;2;158;197;114m▀\x1b[48;2;58;210;70m\x1b[38;2;223;152;89m▀\x1b[48;2;232;139;44m\x1b[38;2;97;121;146m▀\x1b[48;2;233;139;45m\x1b[38;2;140;188;183m▀\x1b[48;2;231;139;44m\x1b[38;2;40;168;8m▀\x1b[48;2;228;140;44m\x1b[38;2;37;169;7m▀\x1b[48;2;227;140;44m\x1b[38;2;36;169;7m▀\x1b[48;2;211;142;41m\x1b[38;2;23;171;5m▀\x1b[48;2;86;161;17m\x1b[38;2;2;174;1m▀\x1b[48;2;0;175;0m \x1b[48;2;0;254;0m\x1b[38;2;190;119;190m▀\x1b[48;2;92;39;23m\x1b[38;2;125;50;114m▀\x1b[48;2;43;246;41m\x1b[38;2;49;10;165m▀\x1b[48;2;12;128;90m\x1b[38;2;209;197;114m▀\x1b[48;2;26;128;90m▀▀▀▀\x1b[48;2;26;128;76m▀\x1b[48;2;26;128;90m\x1b[38;2;209;247;114m▀▀\x1b[38;2;209;197;114m▀\x1b[48;2;26;128;76m\x1b[38;2;209;247;114m▀\x1b[48;2;26;128;90m▀▀▀\x1b[48;2;26;128;76m▀\x1b[48;2;26;128;90m▀▀\x1b[48;2;12;128;76m▀\x1b[48;2;12;113;90m\x1b[38;2;209;247;64m▀\x1b[38;2;209;247;114m▀\x1b[48;2;12;128;90m▀\x1b[48;2;12;113;90m▀\x1b[48;2;12;113;76m\x1b[38;2;209;247;64m▀\x1b[48;2;12;128;90m▀\x1b[48;2;12;113;90m▀\x1b[48;2;12;113;76m\x1b[38;2;209;247;114m▀\x1b[48;2;12;113;90m\x1b[38;2;209;247;64m▀\x1b[48;2;26;128;90m\x1b[38;2;151;129;163m▀\x1b[48;2;115;120;103m\x1b[38;2;62;83;227m▀\x1b[48;2;138;14;25m\x1b[38;2;104;106;160m▀\x1b[48;2;0;0;57m\x1b[38;2;0;0;0m▀\x1b[m
\x1b[48;2;249;147;8m\x1b[38;2;172;69;38m▀\x1b[48;2;197;202;10m\x1b[38;2;82;192;58m▀\x1b[48;2;248;124;45m\x1b[38;2;251;131;47m▀\x1b[48;2;248;124;44m▀\x1b[48;2;248;124;45m▀▀\x1b[48;2;248;124;44m▀\x1b[48;2;248;124;45m▀\x1b[48;2;248;125;45m\x1b[38;2;251;130;47m▀\x1b[48;2;248;124;45m\x1b[38;2;252;130;47m▀\x1b[48;2;248;125;45m\x1b[38;2;252;131;47m▀\x1b[38;2;252;130;47m▀\x1b[38;2;252;131;47m▀▀\x1b[48;2;249;125;45m\x1b[38;2;255;130;48m▀\x1b[48;2;233;127;42m\x1b[38;2;190;141;35m▀\x1b[48;2;57;163;10m\x1b[38;2;13;172;3m▀\x1b[48;2;0;176;0m\x1b[38;2;0;175;0m▀\x1b[48;2;7;174;1m\x1b[38;2;35;169;7m▀\x1b[48;2;178;139;32m\x1b[38;2;220;136;41m▀\x1b[48;2;252;124;45m\x1b[38;2;253;131;47m▀\x1b[48;2;248;125;45m\x1b[38;2;251;131;47m▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀\x1b[48;2;248;125;44m▀\x1b[48;2;248;135;61m\x1b[38;2;251;132;48m▀\x1b[48;2;250;173;122m\x1b[38;2;251;133;50m▀\x1b[48;2;249;155;93m\x1b[38;2;251;132;49m▀\x1b[48;2;248;132;55m\x1b[38;2;251;132;48m▀\x1b[48;2;250;173;122m\x1b[38;2;251;134;51m▀\x1b[48;2;250;163;106m\x1b[38;2;251;134;50m▀\x1b[48;2;248;128;49m\x1b[38;2;251;132;47m▀\x1b[48;2;250;166;110m\x1b[38;2;251;135;52m▀\x1b[48;2;250;175;125m\x1b[38;2;251;136;54m▀\x1b[48;2;248;132;56m\x1b[38;2;251;132;48m▀\x1b[48;2;248;220;160m\x1b[38;2;105;247;172m▀\x1b[48;2;62;101;236m\x1b[38;2;11;207;160m▀\x1b[m
\x1b[48;2;138;181;197m\x1b[38;2;205;36;219m▀\x1b[48;2;177;211;200m\x1b[38;2;83;231;105m▀\x1b[48;2;242;113;40m\x1b[38;2;245;119;42m▀\x1b[48;2;243;113;41m▀\x1b[48;2;245;114;41m▀▀▀▀▀▀▀▀\x1b[38;2;245;119;43m▀▀▀\x1b[48;2;247;114;41m\x1b[38;2;246;119;43m▀\x1b[48;2;202;125;34m\x1b[38;2;143;141;25m▀\x1b[48;2;84;154;14m\x1b[38;2;97;152;17m▀\x1b[48;2;36;166;6m▀\x1b[48;2;139;140;23m\x1b[38;2;183;133;32m▀\x1b[48;2;248;114;41m\x1b[38;2;248;118;43m▀\x1b[48;2;245;115;41m\x1b[38;2;245;119;43m▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀\x1b[38;2;245;119;42m▀\x1b[48;2;246;117;44m\x1b[38;2;246;132;62m▀\x1b[48;2;246;123;54m\x1b[38;2;249;180;138m▀\x1b[48;2;246;120;49m\x1b[38;2;247;157;102m▀\x1b[48;2;246;116;42m\x1b[38;2;246;127;54m▀\x1b[48;2;246;121;50m\x1b[38;2;248;174;128m▀\x1b[48;2;246;120;48m\x1b[38;2;248;162;110m▀\x1b[48;2;246;116;41m\x1b[38;2;245;122;47m▀\x1b[48;2;246;118;46m\x1b[38;2;248;161;108m▀\x1b[48;2;244;118;47m\x1b[38;2;248;171;123m▀\x1b[48;2;243;115;42m\x1b[38;2;246;127;54m▀\x1b[48;2;179;52;29m\x1b[38;2;86;152;223m▀\x1b[48;2;141;225;95m\x1b[38;2;247;146;130m▀\x1b[m
\x1b[48;2;50;237;108m\x1b[38;2;94;70;153m▀\x1b[48;2;206;221;133m\x1b[38;2;64;240;39m▀\x1b[48;2;233;100;36m\x1b[38;2;240;107;38m▀\x1b[48;2;114;56;22m\x1b[38;2;230;104;37m▀\x1b[48;2;24;20;10m\x1b[38;2;193;90;33m▀\x1b[48;2;21;19;9m\x1b[38;2;186;87;32m▀▀▀▀▀▀▀\x1b[38;2;186;87;33m▀▀▀\x1b[48;2;22;18;10m\x1b[38;2;189;86;33m▀\x1b[48;2;18;36;8m\x1b[38;2;135;107;24m▀\x1b[48;2;3;153;2m\x1b[38;2;5;171;1m▀\x1b[48;2;0;177;0m \x1b[48;2;4;158;2m\x1b[38;2;69;147;12m▀\x1b[48;2;19;45;8m\x1b[38;2;185;89;32m▀\x1b[48;2;22;17;10m\x1b[38;2;186;87;33m▀\x1b[48;2;21;19;9m▀▀▀▀▀▀▀▀\x1b[48;2;21;19;10m▀▀\x1b[48;2;21;19;9m▀▀▀▀\x1b[48;2;21;19;10m▀▀▀\x1b[38;2;186;87;32m▀▀\x1b[48;2;21;19;9m\x1b[38;2;186;87;33m▀\x1b[48;2;21;19;10m\x1b[38;2;186;87;32m▀▀\x1b[48;2;21;19;9m\x1b[38;2;186;87;33m▀\x1b[48;2;22;19;10m\x1b[38;2;191;89;33m▀\x1b[48;2;95;49;20m\x1b[38;2;226;103;37m▀\x1b[48;2;227;99;36m\x1b[38;2;241;109;39m▀\x1b[48;2;80;140;154m\x1b[38;2;17;240;92m▀\x1b[48;2;221;58;175m\x1b[38;2;71;14;245m▀\x1b[m
\x1b[48;2;195;38;42m\x1b[38;2;5;126;86m▀\x1b[48;2;139;230;67m\x1b[38;2;253;201;228m▀\x1b[48;2;208;82;30m\x1b[38;2;213;89;32m▀\x1b[48;2;42;26;12m\x1b[38;2;44;27;12m▀\x1b[48;2;9;14;7m\x1b[38;2;8;13;7m▀\x1b[48;2;11;15;8m\x1b[38;2;10;14;7m▀▀▀▀▀▀▀▀▀▀▀\x1b[48;2;11;12;8m\x1b[38;2;10;17;7m▀\x1b[48;2;7;71;5m\x1b[38;2;4;120;3m▀\x1b[48;2;1;164;1m\x1b[38;2;0;178;0m▀\x1b[48;2;4;118;3m\x1b[38;2;0;177;0m▀\x1b[48;2;5;108;3m\x1b[38;2;4;116;3m▀\x1b[48;2;7;75;5m\x1b[38;2;10;23;7m▀\x1b[48;2;10;33;7m\x1b[38;2;10;12;7m▀\x1b[48;2;11;13;8m\x1b[38;2;10;14;7m▀\x1b[48;2;11;14;8m▀\x1b[48;2;11;15;8m▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀\x1b[48;2;10;14;7m\x1b[38;2;9;14;7m▀\x1b[48;2;30;21;10m\x1b[38;2;30;22;10m▀\x1b[48;2;195;79;29m\x1b[38;2;200;84;31m▀\x1b[48;2;205;228;23m\x1b[38;2;111;40;217m▀\x1b[48;2;9;217;69m\x1b[38;2;115;137;104m▀\x1b[m
\x1b[48;2;106;72;209m\x1b[38;2;151;183;253m▀\x1b[48;2;120;239;0m\x1b[38;2;25;2;162m▀\x1b[48;2;203;72;26m\x1b[38;2;206;77;28m▀\x1b[48;2;42;24;11m\x1b[38;2;42;25;11m▀\x1b[48;2;9;14;7m \x1b[48;2;11;15;8m           \x1b[38;2;11;14;8m▀\x1b[48;2;11;13;8m\x1b[38;2;10;28;7m▀\x1b[48;2;9;36;6m\x1b[38;2;7;78;5m▀\x1b[48;2;2;153;1m\x1b[38;2;6;94;4m▀\x1b[48;2;0;178;0m\x1b[38;2;2;156;1m▀\x1b[48;2;0;175;0m\x1b[38;2;1;167;1m▀\x1b[48;2;0;177;0m\x1b[38;2;2;145;2m▀\x1b[48;2;2;147;2m\x1b[38;2;8;54;6m▀\x1b[48;2;9;38;6m\x1b[38;2;11;13;8m▀\x1b[48;2;11;13;8m\x1b[38;2;11;14;8m▀\x1b[48;2;11;15;8m                   \x1b[48;2;10;14;7m \x1b[48;2;29;20;10m\x1b[38;2;29;21;10m▀\x1b[48;2;190;69;25m\x1b[38;2;193;74;27m▀\x1b[48;2;136;91;148m\x1b[38;2;42;159;86m▀\x1b[48;2;89;85;149m\x1b[38;2;160;5;219m▀\x1b[m
\x1b[48;2;229;106;143m\x1b[38;2;40;239;187m▀\x1b[48;2;196;134;237m\x1b[38;2;6;11;95m▀\x1b[48;2;197;60;22m\x1b[38;2;201;67;24m▀\x1b[48;2;41;22;10m\x1b[38;2;41;23;11m▀\x1b[48;2;9;14;7m \x1b[48;2;11;15;8m   \x1b[48;2;10;14;7m\x1b[38;2;11;15;8m▀▀\x1b[48;2;11;15;8m       \x1b[38;2;11;14;8m▀\x1b[48;2;11;14;8m\x1b[38;2;11;16;7m▀\x1b[48;2;11;15;7m\x1b[38;2;7;79;5m▀\x1b[48;2;7;68;5m\x1b[38;2;1;164;1m▀\x1b[48;2;2;153;1m\x1b[38;2;0;176;0m▀\x1b[48;2;2;154;1m\x1b[38;2;0;175;0m▀\x1b[48;2;5;107;3m\x1b[38;2;1;171;1m▀\x1b[48;2;4;115;3m\x1b[38;2;5;105;3m▀\x1b[48;2;6;84;4m\x1b[38;2;11;18;7m▀\x1b[48;2;10;30;7m\x1b[38;2;11;13;8m▀\x1b[48;2;11;13;8m\x1b[38;2;11;15;8m▀\x1b[48;2;11;14;8m▀\x1b[48;2;11;15;8m                \x1b[48;2;10;14;7m \x1b[48;2;29;19;9m\x1b[38;2;29;20;10m▀\x1b[48;2;185;58;22m\x1b[38;2;188;64;24m▀\x1b[48;2;68;241;49m\x1b[38;2;199;22;211m▀\x1b[48;2;133;139;8m\x1b[38;2;239;129;78m▀\x1b[m
\x1b[48;2;74;30;32m\x1b[38;2;163;185;76m▀\x1b[48;2;110;172;9m\x1b[38;2;177;1;123m▀\x1b[48;2;189;43;16m\x1b[38;2;193;52;19m▀\x1b[48;2;39;20;9m\x1b[38;2;40;21;10m▀\x1b[48;2;9;14;7m \x1b[48;2;11;15;8m \x1b[48;2;11;14;7m\x1b[38;2;11;15;8m▀\x1b[48;2;9;14;7m\x1b[38;2;11;14;8m▀\x1b[48;2;106;54;38m\x1b[38;2;31;24;15m▀\x1b[48;2;164;71;49m\x1b[38;2;24;20;12m▀\x1b[48;2;94;46;31m\x1b[38;2;8;14;7m▀\x1b[48;2;36;24;15m\x1b[38;2;9;14;7m▀\x1b[48;2;11;15;8m\x1b[38;2;11;14;7m▀\x1b[48;2;8;14;7m\x1b[38;2;11;15;8m▀\x1b[48;2;10;14;7m▀\x1b[48;2;11;15;8m    \x1b[38;2;11;14;8m▀\x1b[48;2;11;14;8m\x1b[38;2;11;13;8m▀\x1b[48;2;11;13;8m\x1b[38;2;9;45;6m▀\x1b[48;2;10;19;7m\x1b[38;2;7;75;5m▀\x1b[48;2;6;83;4m\x1b[38;2;2;143;2m▀\x1b[48;2;2;156;1m\x1b[38;2;0;176;0m▀\x1b[48;2;0;177;0m\x1b[38;2;0;175;0m▀\x1b[38;2;3;134;2m▀\x1b[48;2;2;152;1m\x1b[38;2;9;46;6m▀\x1b[48;2;8;60;5m\x1b[38;2;11;13;8m▀\x1b[48;2;11;14;7m\x1b[38;2;11;14;8m▀\x1b[48;2;11;14;8m\x1b[38;2;11;15;8m▀\x1b[48;2;11;15;8m              \x1b[48;2;10;14;7m \x1b[48;2;28;18;9m \x1b[48;2;177;43;16m\x1b[38;2;181;51;19m▀\x1b[48;2;93;35;236m\x1b[38;2;224;10;142m▀\x1b[48;2;72;51;52m\x1b[38;2;213;112;158m▀\x1b[m
\x1b[48;2;175;209;155m\x1b[38;2;7;131;221m▀\x1b[48;2;24;0;85m\x1b[38;2;44;86;152m▀\x1b[48;2;181;27;10m\x1b[38;2;185;35;13m▀\x1b[48;2;38;17;8m\x1b[38;2;39;18;9m▀\x1b[48;2;9;14;7m \x1b[48;2;11;15;8m \x1b[48;2;11;14;7m \x1b[48;2;9;14;7m \x1b[48;2;87;43;32m\x1b[38;2;114;54;39m▀\x1b[48;2;188;71;54m\x1b[38;2;211;82;59m▀\x1b[48;2;203;73;55m\x1b[38;2;204;80;57m▀\x1b[48;2;205;73;55m\x1b[38;2;178;71;51m▀\x1b[48;2;204;74;55m\x1b[38;2;119;52;37m▀\x1b[48;2;188;69;52m\x1b[38;2;54;29;19m▀\x1b[48;2;141;55;41m\x1b[38;2;16;17;9m▀\x1b[48;2;75;35;24m\x1b[38;2;8;14;7m▀\x1b[48;2;26;20;12m\x1b[38;2;10;14;7m▀\x1b[48;2;9;14;7m\x1b[38;2;11;14;7m▀\x1b[38;2;11;15;8m▀\x1b[48;2;11;14;7m▀\x1b[48;2;11;15;8m  \x1b[38;2;11;14;8m▀\x1b[48;2;11;14;8m \x1b[48;2;11;13;8m\x1b[38;2;9;45;6m▀\x1b[48;2;10;23;7m\x1b[38;2;4;123;3m▀\x1b[48;2;7;75;5m\x1b[38;2;1;172;1m▀\x1b[48;2;6;84;4m\x1b[38;2;2;154;1m▀\x1b[48;2;4;114;3m\x1b[38;2;5;107;3m▀\x1b[48;2;5;103;4m\x1b[38;2;10;29;7m▀\x1b[48;2;10;23;7m\x1b[38;2;11;13;8m▀\x1b[48;2;11;14;8m\x1b[38;2;11;15;8m▀\x1b[48;2;11;15;8m             \x1b[48;2;10;14;7m \x1b[48;2;27;16;8m\x1b[38;2;27;17;9m▀\x1b[48;2;170;27;10m\x1b[38;2;174;35;13m▀\x1b[48;2;118;117;199m\x1b[38;2;249;61;74m▀\x1b[48;2;10;219;61m\x1b[38;2;187;245;202m▀\x1b[m
\x1b[48;2;20;155;44m\x1b[38;2;86;54;110m▀\x1b[48;2;195;85;113m\x1b[38;2;214;171;227m▀\x1b[48;2;173;10;4m\x1b[38;2;177;19;7m▀\x1b[48;2;37;14;7m\x1b[38;2;37;16;8m▀\x1b[48;2;9;15;8m\x1b[38;2;9;14;7m▀\x1b[48;2;11;15;8m  \x1b[38;2;11;14;7m▀\x1b[48;2;11;14;7m\x1b[38;2;15;17;9m▀\x1b[48;2;9;14;7m\x1b[38;2;50;29;20m▀\x1b[48;2;10;15;8m\x1b[38;2;112;47;36m▀\x1b[48;2;33;22;15m\x1b[38;2;170;61;48m▀\x1b[48;2;88;38;29m\x1b[38;2;197;66;53m▀\x1b[48;2;151;53;43m\x1b[38;2;201;67;53m▀\x1b[48;2;189;60;50m▀\x1b[48;2;198;60;51m\x1b[38;2;194;65;52m▀\x1b[38;2;160;56;44m▀\x1b[48;2;196;60;50m\x1b[38;2;99;40;30m▀\x1b[48;2;174;55;47m\x1b[38;2;41;24;16m▀\x1b[48;2;122;43;35m\x1b[38;2;12;15;8m▀\x1b[48;2;59;27;20m\x1b[38;2;8;14;7m▀\x1b[48;2;16;16;9m\x1b[38;2;10;14;7m▀\x1b[48;2;10;14;7m\x1b[38;2;11;15;8m▀\x1b[48;2;11;15;8m  \x1b[38;2;11;14;8m▀\x1b[48;2;11;14;8m\x1b[38;2;11;12;8m▀\x1b[48;2;10;25;7m\x1b[38;2;7;79;5m▀\x1b[48;2;3;141;2m\x1b[38;2;1;174;1m▀\x1b[48;2;0;178;0m\x1b[38;2;1;169;1m▀\x1b[48;2;6;88;4m\x1b[38;2;8;56;6m▀\x1b[48;2;11;12;8m \x1b[48;2;11;14;8m\x1b[38;2;11;15;8m▀\x1b[48;2;11;15;8m            \x1b[48;2;10;14;7m \x1b[48;2;26;15;8m\x1b[38;2;27;15;8m▀\x1b[48;2;162;12;5m\x1b[38;2;166;20;8m▀\x1b[48;2;143;168;130m\x1b[38;2;18;142;37m▀\x1b[48;2;240;96;105m\x1b[38;2;125;158;211m▀\x1b[m
\x1b[48;2;54;0;0m\x1b[38;2;187;22;0m▀\x1b[48;2;204;0;0m\x1b[38;2;128;208;0m▀\x1b[48;2;162;1;1m\x1b[38;2;168;3;1m▀\x1b[48;2;35;13;7m\x1b[38;2;36;13;7m▀\x1b[48;2;9;15;8m \x1b[48;2;11;15;8m     \x1b[38;2;11;14;7m▀\x1b[38;2;9;14;7m▀\x1b[38;2;8;14;7m▀\x1b[48;2;10;14;7m\x1b[38;2;21;18;11m▀\x1b[48;2;7;13;6m\x1b[38;2;65;30;23m▀\x1b[48;2;12;16;9m\x1b[38;2;129;45;38m▀\x1b[48;2;57;29;23m\x1b[38;2;176;53;47m▀\x1b[48;2;148;49;44m\x1b[38;2;191;53;48m▀\x1b[48;2;187;52;48m\x1b[38;2;192;53;48m▀\x1b[48;2;186;51;47m\x1b[38;2;194;54;49m▀\x1b[48;2;182;52;47m\x1b[38;2;178;52;46m▀\x1b[48;2;59;27;21m\x1b[38;2;53;26;19m▀\x1b[48;2;8;14;7m \x1b[48;2;11;15;8m  \x1b[48;2;11;14;8m\x1b[38;2;11;15;8m▀\x1b[48;2;11;12;8m\x1b[38;2;11;14;8m▀\x1b[48;2;10;30;7m\x1b[38;2;10;23;7m▀\x1b[48;2;5;110;3m\x1b[38;2;3;138;2m▀\x1b[48;2;2;149;2m\x1b[38;2;0;181;0m▀\x1b[48;2;6;92;4m\x1b[38;2;5;100;4m▀\x1b[48;2;11;13;8m \x1b[48;2;11;14;8m \x1b[48;2;11;15;8m            \x1b[48;2;10;15;8m \x1b[48;2;25;14;7m\x1b[38;2;26;14;7m▀\x1b[48;2;152;2;1m\x1b[38;2;158;5;2m▀\x1b[48;2;6;0;0m\x1b[38;2;44;193;0m▀\x1b[48;2;108;0;0m\x1b[38;2;64;70;0m▀\x1b[m
\x1b[48;2;44;0;0m\x1b[38;2;177;0;0m▀\x1b[48;2;147;0;0m\x1b[38;2;71;0;0m▀\x1b[48;2;148;1;1m\x1b[38;2;155;1;1m▀\x1b[48;2;33;13;7m\x1b[38;2;34;13;7m▀\x1b[48;2;9;15;8m \x1b[48;2;11;15;8m   \x1b[48;2;11;14;7m\x1b[38;2;11;15;8m▀\x1b[48;2;10;14;7m▀\x1b[48;2;9;14;7m▀\x1b[48;2;13;16;9m\x1b[38;2;11;14;7m▀\x1b[48;2;42;24;17m\x1b[38;2;9;14;7m▀\x1b[48;2;97;38;32m\x1b[38;2;10;15;8m▀\x1b[48;2;149;49;44m\x1b[38;2;30;21;14m▀\x1b[48;2;174;52;48m\x1b[38;2;79;34;28m▀\x1b[48;2;178;52;48m\x1b[38;2;136;45;40m▀\x1b[38;2;172;51;47m▀\x1b[48;2;173;52;48m\x1b[38;2;181;52;48m▀\x1b[48;2;147;47;42m\x1b[38;2;183;52;48m▀\x1b[48;2;94;35;30m\x1b[38;2;177;52;48m▀\x1b[48;2;25;19;12m\x1b[38;2;56;27;20m▀\x1b[48;2;10;14;7m\x1b[38;2;8;14;7m▀\x1b[48;2;11;12;8m\x1b[38;2;11;15;8m▀\x1b[48;2;10;23;7m\x1b[38;2;11;14;8m▀\x1b[48;2;7;76;5m\x1b[38;2;11;13;8m▀\x1b[48;2;2;152;1m\x1b[38;2;9;45;6m▀\x1b[48;2;0;177;0m\x1b[38;2;5;106;3m▀\x1b[48;2;0;178;0m\x1b[38;2;4;123;3m▀\x1b[48;2;1;168;1m\x1b[38;2;5;104;3m▀\x1b[48;2;8;53;6m\x1b[38;2;9;47;6m▀\x1b[48;2;11;12;8m\x1b[38;2;11;13;8m▀\x1b[48;2;11;15;8m             \x1b[48;2;10;15;8m \x1b[48;2;24;14;7m\x1b[38;2;25;14;7m▀\x1b[48;2;140;2;1m\x1b[38;2;146;2;1m▀\x1b[48;2;219;0;0m\x1b[38;2;225;0;0m▀\x1b[48;2;126;0;0m\x1b[38;2;117;0;0m▀\x1b[m
\x1b[48;2;34;0;0m\x1b[38;2;167;0;0m▀\x1b[48;2;89;0;0m\x1b[38;2;14;0;0m▀\x1b[48;2;134;1;1m\x1b[38;2;141;1;1m▀\x1b[48;2;31;13;7m\x1b[38;2;32;13;7m▀\x1b[48;2;10;15;8m \x1b[48;2;11;15;8m \x1b[48;2;11;14;7m\x1b[38;2;11;15;8m▀\x1b[48;2;10;14;7m\x1b[38;2;11;14;7m▀\x1b[48;2;53;29;22m\x1b[38;2;10;14;7m▀\x1b[48;2;127;46;41m\x1b[38;2;20;18;11m▀\x1b[48;2;158;51;47m\x1b[38;2;57;28;22m▀\x1b[48;2;166;52;48m\x1b[38;2;113;42;36m▀\x1b[48;2;167;52;48m\x1b[38;2;156;50;46m▀\x1b[48;2;164;52;48m\x1b[38;2;171;52;48m▀\x1b[48;2;146;48;44m\x1b[38;2;172;52;48m▀\x1b[48;2;102;38;33m▀\x1b[48;2;50;26;19m\x1b[38;2;161;51;46m▀\x1b[48;2;17;17;10m\x1b[38;2;126;44;38m▀\x1b[48;2;8;14;7m\x1b[38;2;71;31;25m▀\x1b[48;2;10;14;7m\x1b[38;2;27;19;13m▀\x1b[48;2;11;13;8m\x1b[38;2;10;14;7m▀\x1b[48;2;9;40;6m\x1b[38;2;10;13;7m▀\x1b[48;2;4;119;3m\x1b[38;2;11;20;7m▀\x1b[48;2;1;168;1m\x1b[38;2;8;63;5m▀\x1b[48;2;0;177;0m\x1b[38;2;3;130;2m▀\x1b[48;2;0;175;0m\x1b[38;2;1;171;1m▀\x1b[48;2;1;174;1m\x1b[38;2;0;176;0m▀\x1b[48;2;1;175;1m\x1b[38;2;1;174;1m▀\x1b[48;2;0;177;0m\x1b[38;2;0;176;0m▀\x1b[48;2;3;134;2m\x1b[38;2;2;158;1m▀\x1b[48;2;10;21;7m\x1b[38;2;9;38;6m▀\x1b[48;2;11;14;8m\x1b[38;2;11;13;8m▀\x1b[48;2;11;15;8m             \x1b[48;2;10;15;8m \x1b[48;2;23;14;7m \x1b[48;2;127;2;1m\x1b[38;2;133;2;1m▀\x1b[48;2;176;0;0m\x1b[38;2;213;0;0m▀\x1b[48;2;109;0;0m\x1b[38;2;100;0;0m▀\x1b[m
\x1b[48;2;24;0;0m\x1b[38;2;157;0;0m▀\x1b[48;2;32;0;0m\x1b[38;2;165;0;0m▀\x1b[48;2;121;1;1m\x1b[38;2;128;1;1m▀\x1b[48;2;28;13;7m\x1b[38;2;30;13;7m▀\x1b[48;2;10;15;8m \x1b[48;2;11;15;8m \x1b[48;2;11;14;7m \x1b[48;2;9;15;7m \x1b[48;2;88;41;34m\x1b[38;2;91;41;34m▀\x1b[48;2;145;51;47m\x1b[38;2;163;53;49m▀\x1b[48;2;107;42;36m\x1b[38;2;161;52;48m▀\x1b[48;2;58;29;22m\x1b[38;2;155;51;47m▀\x1b[48;2;21;18;11m\x1b[38;2;128;45;40m▀\x1b[48;2;9;14;7m\x1b[38;2;79;33;27m▀\x1b[38;2;33;21;15m▀\x1b[48;2;11;14;7m\x1b[38;2;12;15;8m▀\x1b[48;2;11;15;8m\x1b[38;2;9;14;7m▀\x1b[38;2;10;14;7m▀ \x1b[48;2;11;12;8m\x1b[38;2;11;14;8m▀\x1b[48;2;8;54;6m\x1b[38;2;10;28;7m▀\x1b[48;2;6;93;4m\x1b[38;2;4;125;3m▀\x1b[48;2;2;152;1m\x1b[38;2;0;175;0m▀\x1b[48;2;0;176;0m▀\x1b[48;2;0;175;0m\x1b[38;2;1;174;1m▀\x1b[48;2;0;177;0m\x1b[38;2;1;175;1m▀\x1b[48;2;0;175;0m▀▀\x1b[48;2;1;162;1m\x1b[38;2;0;176;0m▀\x1b[48;2;9;47;6m\x1b[38;2;6;95;4m▀\x1b[48;2;11;13;8m \x1b[48;2;11;15;8m\x1b[38;2;11;14;8m▀             \x1b[48;2;10;15;8m \x1b[48;2;21;13;7m\x1b[38;2;22;13;7m▀\x1b[48;2;114;2;1m\x1b[38;2;121;2;1m▀\x1b[48;2;164;0;0m\x1b[38;2;170;0;0m▀\x1b[48;2;127;0;0m\x1b[38;2;118;0;0m▀\x1b[m
\x1b[48;2;14;0;0m\x1b[38;2;147;0;0m▀\x1b[48;2;183;0;0m\x1b[38;2;108;0;0m▀\x1b[48;2;107;1;1m\x1b[38;2;114;1;1m▀\x1b[48;2;26;13;7m\x1b[38;2;27;13;7m▀\x1b[48;2;10;15;8m \x1b[48;2;11;15;8m \x1b[38;2;11;14;7m▀ \x1b[48;2;10;14;7m\x1b[38;2;43;27;20m▀\x1b[48;2;9;14;7m\x1b[38;2;42;25;18m▀\x1b[48;2;11;14;7m\x1b[38;2;14;16;9m▀\x1b[48;2;11;15;8m\x1b[38;2;9;14;7m▀\x1b[38;2;10;14;7m▀\x1b[38;2;11;14;7m▀     \x1b[48;2;11;12;8m \x1b[48;2;9;49;6m\x1b[38;2;8;64;5m▀\x1b[48;2;1;166;1m\x1b[38;2;1;159;1m▀\x1b[48;2;0;175;0m\x1b[38;2;1;171;1m▀ \x1b[48;2;1;159;1m\x1b[38;2;1;167;1m▀\x1b[48;2;7;79;5m\x1b[38;2;4;122;3m▀\x1b[48;2;2;144;2m\x1b[38;2;2;158;1m▀\x1b[48;2;0;158;1m\x1b[38;2;0;177;0m▀\x1b[48;2;7;44;6m\x1b[38;2;4;112;3m▀\x1b[48;2;9;12;7m\x1b[38;2;11;17;7m▀\x1b[48;2;9;14;7m\x1b[38;2;11;14;8m▀\x1b[38;2;11;15;8m▀▀▀▀▀▀▀▀▀▀▀\x1b[48;2;11;14;7m▀\x1b[48;2;11;15;8m  \x1b[48;2;10;15;8m \x1b[48;2;20;13;7m\x1b[38;2;21;13;7m▀\x1b[48;2;102;2;1m\x1b[38;2;108;2;1m▀\x1b[48;2;121;0;0m\x1b[38;2;127;0;0m▀\x1b[48;2;146;0;0m\x1b[38;2;136;0;0m▀\x1b[m
\x1b[48;2;3;0;0m\x1b[38;2;137;0;0m▀\x1b[48;2;173;0;0m\x1b[38;2;50;0;0m▀\x1b[48;2;93;1;1m\x1b[38;2;100;1;1m▀\x1b[48;2;24;13;7m\x1b[38;2;25;13;7m▀\x1b[48;2;10;15;8m \x1b[48;2;11;15;8m            \x1b[48;2;11;14;7m\x1b[38;2;11;15;8m▀▀\x1b[48;2;17;14;7m\x1b[38;2;11;14;8m▀\x1b[48;2;49;12;7m\x1b[38;2;9;24;7m▀\x1b[48;2;62;54;4m\x1b[38;2;8;133;2m▀\x1b[48;2;7;159;1m\x1b[38;2;2;176;0m▀\x1b[48;2;0;175;0m \x1b[48;2;1;172;1m\x1b[38;2;0;175;0m▀\x1b[48;2;1;159;1m\x1b[38;2;0;173;1m▀\x1b[48;2;46;122;19m\x1b[38;2;1;176;0m▀\x1b[48;2;122;63;45m\x1b[38;2;45;111;18m▀\x1b[48;2;135;52;49m\x1b[38;2;75;36;31m▀\x1b[48;2;135;53;49m\x1b[38;2;74;36;30m▀▀▀▀▀▀▀▀▀▀▀\x1b[48;2;136;53;49m\x1b[38;2;75;37;31m▀\x1b[48;2;119;49;45m\x1b[38;2;66;34;28m▀\x1b[48;2;25;20;13m\x1b[38;2;18;18;11m▀\x1b[48;2;10;14;7m \x1b[48;2;11;15;8m \x1b[48;2;10;15;8m \x1b[48;2;19;13;7m \x1b[48;2;89;2;1m\x1b[38;2;95;2;1m▀\x1b[48;2;77;0;0m\x1b[38;2;83;0;0m▀\x1b[48;2;128;0;0m\x1b[38;2;119;0;0m▀\x1b[m
\x1b[48;2;60;0;0m\x1b[38;2;126;0;0m▀\x1b[48;2;182;0;0m\x1b[38;2;249;0;0m▀\x1b[48;2;83;1;1m\x1b[38;2;87;1;1m▀\x1b[48;2;22;13;7m\x1b[38;2;23;13;7m▀\x1b[48;2;10;15;8m \x1b[48;2;11;15;8m            \x1b[48;2;11;14;7m\x1b[38;2;16;14;7m▀\x1b[48;2;14;14;7m\x1b[38;2;42;13;7m▀\x1b[48;2;58;13;6m\x1b[38;2;95;11;5m▀\x1b[48;2;34;13;7m\x1b[38;2;100;11;5m▀\x1b[48;2;9;14;7m\x1b[38;2;21;17;7m▀\x1b[48;2;11;12;8m\x1b[38;2;8;55;6m▀\x1b[38;2;7;75;5m▀\x1b[38;2;8;65;5m▀\x1b[48;2;11;13;8m\x1b[38;2;9;41;6m▀\x1b[48;2;12;15;8m\x1b[38;2;60;37;28m▀\x1b[38;2;90;42;37m▀\x1b[38;2;88;42;36m▀▀▀▀▀▀▀▀▀▀▀▀\x1b[38;2;89;42;37m▀\x1b[38;2;78;39;33m▀\x1b[48;2;11;15;8m\x1b[38;2;20;18;11m▀\x1b[48;2;11;14;7m\x1b[38;2;10;14;7m▀\x1b[48;2;11;15;8m \x1b[48;2;10;15;8m \x1b[48;2;18;13;7m \x1b[48;2;78;2;1m\x1b[38;2;83;2;1m▀\x1b[48;2;196;0;0m\x1b[38;2;40;0;0m▀\x1b[48;2;217;0;0m\x1b[38;2;137;0;0m▀\x1b[m
\x1b[48;2;227;0;0m\x1b[38;2;16;0;0m▀\x1b[48;2;116;0;0m\x1b[38;2;21;0;0m▀\x1b[48;2;79;1;1m\x1b[38;2;81;1;1m▀\x1b[48;2;22;13;7m \x1b[48;2;10;15;8m \x1b[48;2;11;15;8m             \x1b[38;2;10;15;8m▀\x1b[48;2;10;15;8m\x1b[38;2;21;14;7m▀\x1b[48;2;11;15;8m\x1b[38;2;14;14;7m▀\x1b[38;2;11;14;7m▀    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀  \x1b[48;2;10;15;8m \x1b[48;2;17;13;7m\x1b[38;2;18;13;7m▀\x1b[48;2;75;2;1m\x1b[38;2;76;2;1m▀\x1b[48;2;97;0;0m\x1b[38;2;34;0;0m▀\x1b[48;2;76;0;0m\x1b[38;2;147;0;0m▀\x1b[m
\x1b[48;2;161;0;0m\x1b[38;2;183;0;0m▀\x1b[48;2;49;0;0m\x1b[38;2;211;0;0m▀\x1b[48;2;75;1;1m\x1b[38;2;77;1;1m▀\x1b[48;2;21;13;7m \x1b[48;2;10;15;8m \x1b[48;2;11;15;8m                                        \x1b[48;2;10;15;8m \x1b[48;2;17;13;7m \x1b[48;2;71;2;1m\x1b[38;2;73;2;1m▀\x1b[48;2;253;0;0m\x1b[38;2;159;0;0m▀\x1b[48;2;191;0;0m\x1b[38;2;5;0;0m▀\x1b[m
\x1b[48;2;110;161;100m\x1b[38;2;116;0;0m▀\x1b[48;2;9;205;205m\x1b[38;2;192;0;0m▀\x1b[48;2;78;0;0m\x1b[38;2;77;1;0m▀\x1b[48;2;66;3;1m\x1b[38;2;30;11;6m▀\x1b[48;2;42;8;4m\x1b[38;2;9;15;8m▀\x1b[48;2;39;8;4m\x1b[38;2;10;15;8m▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀\x1b[48;2;40;8;4m▀\x1b[48;2;39;8;4m▀▀▀▀▀▀▀\x1b[48;2;40;8;4m▀▀▀\x1b[48;2;39;8;4m▀\x1b[48;2;40;8;4m▀\x1b[48;2;39;8;4m▀\x1b[48;2;41;8;4m\x1b[38;2;9;15;8m▀\x1b[48;2;62;4;2m\x1b[38;2;24;13;7m▀\x1b[48;2;78;0;0m\x1b[38;2;74;1;1m▀\x1b[48;2;221;222;0m\x1b[38;2;59;0;0m▀\x1b[48;2;67;199;133m\x1b[38;2;85;0;0m▀\x1b[m
\x1b[48;2;0;0;0m\x1b[38;2;143;233;149m▀\x1b[48;2;108;184;254m\x1b[38;2;213;6;76m▀\x1b[48;2;197;183;82m\x1b[38;2;76;0;0m▀\x1b[48;2;154;157;0m▀\x1b[48;2;96;0;0m▀\x1b[48;2;253;0;0m▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀\x1b[48;2;226;0;0m▀\x1b[48;2;255;127;255m▀\x1b[48;2;84;36;66m\x1b[38;2;64;247;251m▀\x1b[48;2;0;0;0m\x1b[38;2;18;76;210m▀\x1b[m
\x1b[48;2;0;0;0m                                                  \x1b[m
\x1b[48;2;0;0;0m                                                  \x1b[m
"""
)

if __name__ == "__main__":
    main()
