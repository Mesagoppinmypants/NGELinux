package script.spawning.tatooine.mos_eisley;

import script.*;
import script.base_class.*;
import script.combat_engine.*;
import java.util.Arrays;
import java.util.Hashtable;
import java.util.Vector;
import script.base_script;

import script.library.create;
import script.library.ai_lib;
import script.library.performance;

public class mos_eisley_mayor_building extends script.base_script
{
    public mos_eisley_mayor_building()
    {
    }
    public int OnInitialize(obj_id self) throws InterruptedException
    {
        debugServerConsoleMsg(self, "Initialized Mos Eisley Mayor Building Spawner Script");
        dictionary params = new dictionary();
        messageTo(self, "spawnThings", null, 1, true);
        return SCRIPT_CONTINUE;
    }
    public void spawnEveryone(obj_id self) throws InterruptedException
    {
        spawnMayor(self);
        spawnNewbiePilotHelper(self);
        return;
    }
    public void spawnMayor(obj_id self) throws InterruptedException
    {
        obj_id room = getCellId(self, "mainroom");
        location mayor_loc = new location(0.1f, 2.5f, 7.5f, "tatooine", room);
        int mayor_yaw = 180;
        obj_id mayor = create.object("mos_eisley_mayor", mayor_loc);
        setYaw(mayor, mayor_yaw);
        setCreatureStatic(mayor, true);
        attachScript(mayor, "conversation.mos_eisley_mayor");
        return;
    }
    public void spawnNewbiePilotHelper(obj_id self) throws InterruptedException
    {
        obj_id room = getCellId(self, "mainroom");
        location pilot_loc = new location(-1.9f, 1.1f, -5.7f, "tatooine", room);
        int pilot_yaw = 2;
        obj_id pilot = create.object("newbie_pilot_informer", pilot_loc);
        setYaw(pilot, pilot_yaw);
        setCreatureStatic(pilot, true);
        return;
    }
    public int spawnThings(obj_id self, dictionary params) throws InterruptedException
    {
        spawnEveryone(self);
        return SCRIPT_CONTINUE;
    }
}
