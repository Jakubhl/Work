Pro správný logging, tohle musí být v: Scene control macro tool:

Rem *******************************************
Rem McrInit Subroutine
Rem *******************************************

*MCRINIT
SY.CURRENT_SCENE&=SceneNo
SY.SCENE_NAME$ = SceneTitle$(SY.CURRENT_SCENE&)
Return
