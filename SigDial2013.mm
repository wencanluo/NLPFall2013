<map version="1.0.1">
<!-- To view this file, download free mind mapping software FreeMind from http://freemind.sourceforge.net -->
<node CREATED="1379948860941" ID="ID_1863728081" MODIFIED="1380067236695" STYLE="bubble" TEXT="SigDial2013">
<node CREATED="1379948886432" ID="ID_1950858520" MODIFIED="1379948905723" POSITION="right" STYLE="bubble" TEXT="Classification Model">
<node CREATED="1379948900584" ID="ID_508409351" MODIFIED="1379948910831" STYLE="bubble" TEXT="Features">
<node CREATED="1379948912065" ID="ID_1668303081" MODIFIED="1379948940462" TEXT="dialog_state"/>
</node>
<node CREATED="1380066652304" ID="ID_1457267080" MODIFIED="1380066671108" TEXT="Judge Whether Each Hypo is correct?">
<node CREATED="1380066751725" ID="ID_1634841414" MODIFIED="1380066758503" TEXT="ranking the hypo"/>
</node>
</node>
<node CREATED="1380066886973" ID="ID_689570656" MODIFIED="1380066889378" POSITION="right" TEXT="NLU Model"/>
<node CREATED="1379948959690" ID="ID_1261975336" MODIFIED="1379948968702" POSITION="right" TEXT="Hierarchical Model">
<node CREATED="1379948970233" ID="ID_1779682661" MODIFIED="1380066740356" TEXT="Identify Slot First">
<node CREATED="1380066722911" ID="ID_473729987" MODIFIED="1380066736155" TEXT="Whether the slot appears"/>
</node>
<node CREATED="1379948978027" ID="ID_1642390129" MODIFIED="1379948985452" TEXT="Identify Slot Value"/>
</node>
<node CREATED="1379949025381" ID="ID_1556211358" MODIFIED="1380157399700" POSITION="right" TEXT="Matching Different Dialog Systems">
<node CREATED="1379949044322" ID="ID_1366145783" MODIFIED="1379949050447" TEXT="Match the dialog states"/>
</node>
<node CREATED="1379949086077" ID="ID_1242965173" MODIFIED="1379949655446" POSITION="right" TEXT="Add BusSchedule Fact">
<node CREATED="1379949097193" ID="ID_487056893" MODIFIED="1379949104388" TEXT="Street Names"/>
</node>
<node CREATED="1380125078611" ID="ID_1166420442" MODIFIED="1380125082844" POSITION="right" TEXT="Clustering Model">
<node CREATED="1380125083719" ID="ID_621755595" MODIFIED="1380125092059" TEXT="Group the ASR and SLU results">
<node CREATED="1380125100057" ID="ID_1453400602" MODIFIED="1380125111756" TEXT="phone dictionary"/>
</node>
</node>
<node CREATED="1379949656259" ID="ID_349928610" MODIFIED="1379979156636" POSITION="right" TEXT="Todo">
<node CREATED="1379949660403" ID="ID_931389887" MODIFIED="1379949665203" TEXT="TopLine of NBest">
<node CREATED="1380066848679" ID="ID_443531704" MODIFIED="1380066860142" TEXT="What&apos;s the average rank of correct NLU?"/>
<node CREATED="1380075954212" ID="ID_1778840571" MODIFIED="1380075998613" TEXT="How to combine joint for N-Best?">
<icon BUILTIN="help"/>
<node CREATED="1380075981636" ID="ID_1451544037" MODIFIED="1380075988633" TEXT="Use the topOne"/>
<node CREATED="1380079975266" ID="ID_1105834485" MODIFIED="1380079982606" TEXT="remove duplicate"/>
</node>
<node CREATED="1380138421623" ID="ID_311630762" MODIFIED="1380138433994" TEXT="Slot Conflict in NBest">
<node CREATED="1380138434615" ID="ID_752020702" MODIFIED="1380138446258" TEXT="Only One Slot can be right at one time"/>
</node>
<node CREATED="1380077780710" ID="ID_1533232787" MODIFIED="1380077798030" TEXT="GroupA">
<node CREATED="1380077798779" ID="ID_560590619" MODIFIED="1380077803152" TEXT="used batch data"/>
<node CREATED="1380077805073" ID="ID_69037217" MODIFIED="1380077812179" TEXT="live only has top1"/>
</node>
</node>
<node CREATED="1380122956919" ID="ID_827690030" MODIFIED="1380122968899" TEXT="No-History Model">
<icon BUILTIN="button_ok"/>
</node>
<node CREATED="1379949665563" ID="ID_576944673" MODIFIED="1379949678432" TEXT="Distribution of Slot values"/>
<node CREATED="1379951341270" ID="ID_1937136973" MODIFIED="1379951345488" TEXT="No-Correct Model"/>
<node CREATED="1379979159307" ID="ID_543529692" MODIFIED="1379984631943" TEXT="Get Correct Label for each turn"/>
<node CREATED="1379989274948" ID="ID_1907282153" MODIFIED="1380067005556" TEXT="Turn-level">
<node CREATED="1380067006431" ID="ID_1510631284" MODIFIED="1380067006962" TEXT="Trainscription"/>
<node CREATED="1380066982708" ID="ID_617603117" MODIFIED="1380066987737" TEXT="Dialog acts"/>
<node CREATED="1380067010757" ID="ID_1748716998" MODIFIED="1380067012397" TEXT="Slot"/>
<node CREATED="1380067012990" ID="ID_1483207886" MODIFIED="1380067016239" TEXT="Values"/>
</node>
</node>
<node CREATED="1379957212832" ID="ID_890427419" MODIFIED="1379957215019" POSITION="left" TEXT="Scripts">
<node CREATED="1379957215831" ID="ID_1803875561" MODIFIED="1379957216175" TEXT="dataset_walker">
<node CREATED="1379957217190" ID="ID_835075484" MODIFIED="1379957218330" TEXT="input">
<node CREATED="1379957227656" ID="ID_1840985838" MODIFIED="1379957230936" TEXT="dataset"/>
<node CREATED="1379957232342" ID="ID_138288222" MODIFIED="1379957235419" TEXT="labels"/>
<node CREATED="1379957236544" ID="ID_385844516" MODIFIED="1379957238606" TEXT="dataroot"/>
</node>
<node CREATED="1379957220174" ID="ID_1753830065" MODIFIED="1380066603609" TEXT="output"/>
</node>
<node CREATED="1379963322478" ID="ID_1489646073" MODIFIED="1379963324431" TEXT="QA">
<node CREATED="1379963325290" ID="ID_962540854" MODIFIED="1379963333053" TEXT="joint / all?"/>
<node CREATED="1379978751211" ID="ID_1431396996" MODIFIED="1379978760395" TEXT="GetTurnSchedulesGroundedSlot"/>
</node>
</node>
</node>
</map>
