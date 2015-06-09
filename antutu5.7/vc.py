import re
import sys
import os
import time
from subprocess import call

from com.dtmilano.android.viewclient import ViewClient, ViewNotFoundException

parent_dir = os.path.realpath(os.path.dirname(__file__))
f_output_result="%s/../common/output-test-result.sh"  % parent_dir


kwargs1 = {'verbose': False, 'ignoresecuredevice': False}
device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
kwargs2 = {'startviewserver': True, 'forceviewserveruse': False, 'autodump': False, 'ignoreuiautomatorkilled': True, 'compresseddump': False}
vc = ViewClient(device, serialno, **kwargs2)


def dump_always():
    success = False
    while not success:
        try:
            vc.dump()
            success = True
        except RuntimeError:
            print("Got RuntimeError when call vc.dump()")
            time.sleep(5)
        except ValueError:
            print("Got ValueError when call vc.dump()")
            time.sleep(5)


def switch_arch():
    dump_always()
    settings_button = vc.findViewById("com.antutu.ABenchMark:id/right_action_layout")
    if settings_button:
        settings_button.touch()
        time.sleep(2)
        dump_always()
        switch_to_32bit_btn = vc.findViewWithText(u'Switch to 32-bit')
        switch_to_64bit_btn = vc.findViewWithText(u'Switch to 64-bit')
        switch_btn = None
        if switch_to_64bit_btn:
            prefix = "64bit"
            switch_btn = switch_to_64bit_btn
        elif switch_to_32bit_btn:
            prefix = "32bit"
            switch_btn = switch_to_32bit_btn
        else:
            prefix = "32bit"
            switch_btn = None

        if switch_btn:
            switch_btn.touch()
            can_switch = True
        else:
            device.press("BACK")
            can_switch = False
    else:
        prefix = "32bit"
        can_switch = False

    return (prefix, can_switch)


def run_test(prefix=""):

    #Start all test button
    time.sleep(2)
    dump_always()
    start_test_button = vc.findViewById("com.antutu.ABenchMark:id/start_test_text")
    if start_test_button:
        start_test_button.touch()
    else:
        retest_btn = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/retest_text")
        if retest_btn:
            retest_btn.touch()
        else:
            print("com.antutu.ABenchMark:id/retest_text not found")
            
        time.sleep(2)
        dump_always()
        retest_btn = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/retest_btn")
        if retest_btn:
            retest_btn.touch()
        else:
            print("com.antutu.ABenchMark:id/retest_btn not found")

    time.sleep(5)

    #Wait while antutu5.6.2 is running benchmark
    to_detail = False
    while(not to_detail):
        try:
            time.sleep(30)
            dump_always()
            if vc.findViewWithText('Details - v5.7'):
                to_detail = True
                print("Already in the details page")
            elif vc.findViewById("com.antutu.ABenchMark:id/detail_btn"):
                detail_btn = vc.findViewById("com.antutu.ABenchMark:id/detail_btn")
                detail_btn.touch()
                to_detail = True
                print("Found the Details button, the test should be run successfully")
            elif vc.findViewWithText('Unfortunately, AnTuTu Benchmark has stopped.'):
                ok_btn = vc.findViewWithTextOrRaise(u'OK')
                ok_btn.touch()
                print("Closed the 'Unfortunately, AnTuTu Benchmark has stopped.' dialog.")
            elif vc.findViewWithText('Benchmarking has stopped unexpectedly. Please try again!'):
                ok_btn = vc.findViewWithTextOrRaise(u'OK')
                ok_btn.touch()
                dump_always()
                retest_btn = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/retest_text")
                retest_btn.touch()
                time.sleep(2)
                dump_always()
                retest_btn = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/retest_btn")
                retest_btn.touch()
                print("Benchmarking has stopped unexpectedly, restart again")
            elif vc.findViewById("com.antutu.ABenchMark:id/start_test_region"):
                # seems not sure? this seems start a new test again
                start_test_button = vc.findViewById("com.antutu.ABenchMark:id/start_test_region")
                start_test_button.touch()
                to_detail = True
                print("Found the Test button again, the test might not be run successfully, or no  network connection")
            else:
                print("Wait for conditions to go to details page")

        except ViewNotFoundException:
            print("Got ViewNotFoundException when go to the detail page while waiting for test finished")
        except RuntimeError:
            print("Got RuntimeError when go to the detail page while waiting for test finished")
        except ValueError:
            print("Got ValueError when go to the detail page while waiting for test finished")

    find_detail = False
    while not find_detail:
        try:
            time.sleep(2)
            dump_always()
            vc.findViewWithTextOrRaise('Details - v5.7')
            close_view = vc.findViewById("com.antutu.ABenchMark:id/close_img_view")
            if close_view:
                close_view.touch()
            find_detail = True
            print("Changed to the detail page successfully")
            get_result(prefix=prefix)
        except ViewNotFoundException:
            print("Got ViewNotFoundException when on the details page")
        except RuntimeError:
            print("Got RuntimeError when on the details page")
        except ValueError:
            print("Got ValueError when on the details page")


def get_result(prefix=""):
    if prefix:
        prefix = "antutu57_%s_" % prefix
    else:
        prefix="antutu57_"
    #Get the score
    antutu_sum = 0;
    dump_always()
    multitask_view = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/ue_multitask_text")
    multitask_score = multitask_view.getText().strip()
    call([f_output_result, "%s_ue_multitask" % prefix, 'pass', multitask_score, 'points'])
    antutu_sum = antutu_sum + int(multitask_score)

    runtime_view = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/ue_dalvik_text")
    runtime_score = runtime_view.getText().strip()
    call([f_output_result, "%s_ue_runtime" % prefix, 'pass', runtime_score, 'points'])
    antutu_sum = antutu_sum + int(runtime_score)

    cpu_multi_integer_view = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/cpu_int_text")
    cpu_multi_integer_score = cpu_multi_integer_view.getText().strip()
    call([f_output_result, "%s_cpu_integer" % prefix, 'pass', cpu_multi_integer_score, 'points'])
    antutu_sum = antutu_sum + int(cpu_multi_integer_score)

    cpu_multi_float_point_view = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/cpu_float_text")
    cpu_multi_float_point_score = cpu_multi_float_point_view.getText().strip()
    call([f_output_result, "%s_cpu_float_point" % prefix, 'pass', cpu_multi_float_point_score, 'points'])
    antutu_sum = antutu_sum + int(cpu_multi_float_point_score)

    device.press('DPAD_DOWN')
    time.sleep(2)
    device.press('DPAD_DOWN')
    time.sleep(2)
    dump_always()

    cpu_single_integer_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/cpu_int_text2")
    call([f_output_result, "%s_single_thread_integer" % prefix, 'pass', cpu_single_integer_score.getText().strip(), 'points'])
    antutu_sum = antutu_sum + int(cpu_single_integer_score.getText().strip())

    cpu_single_float_point_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/cpu_float_text2")
    call([f_output_result, "%s_single_float_point" % prefix, 'pass', cpu_single_float_point_score.getText().strip(), 'points'])
    antutu_sum = antutu_sum + int(cpu_single_float_point_score.getText().strip())

    ram_operation_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/mem_text")
    call([f_output_result, "%s_single_ram_operation" % prefix, 'pass', ram_operation_score.getText().strip(), 'points'])
    antutu_sum = antutu_sum + int(ram_operation_score.getText().strip())

    ram_speed_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/ram_text")
    call([f_output_result, "%s_single_ram_speed" % prefix, 'pass', ram_speed_score.getText().strip(), 'points'])
    antutu_sum = antutu_sum + int(ram_speed_score.getText().strip())

    twod_graphics_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/gpu_2d_text")
    call([f_output_result, "%s_2D_graphics" % prefix, 'pass', twod_graphics_score.getText().strip(), 'points'])
    antutu_sum = antutu_sum + int(twod_graphics_score.getText().strip())

    threed_graphics_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/gpu_3d_text")
    score_3d = threed_graphics_score.getText().strip()
    call([f_output_result, "%s_3D_graphics" % prefix, 'pass', score_3d.split(" ").pop(), 'points'])
    antutu_sum = antutu_sum + int(score_3d.split(" ").pop())

    storage_io_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/io_sdw_text")
    call([f_output_result, "%santutu_storage_io" % prefix, 'pass', storage_io_score.getText().strip(), 'points'])
    antutu_sum = antutu_sum + int(storage_io_score.getText().strip())

    database_io_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/io_db_text")
    call([f_output_result, "%s_database_io" % prefix, 'pass', database_io_score.getText().strip(), 'points'])
    antutu_sum = antutu_sum + int(database_io_score.getText().strip())

    call([f_output_result, "%s_total" % prefix, 'pass', str(antutu_sum), 'points'])


def main():
    #Enable 64-bit
    time.sleep(10)
    dump_always()
    win_enable64 = vc.findViewWithText(u'Enable 64-bit')
    if win_enable64:
        enable_btn = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/btn_ok")
        enable_btn.touch()
        time.sleep(10)
        dump_always()
        install_btn = vc.findViewById("com.android.packageinstaller:id/ok_button")
        if install_btn:
            install_btn.touch()
            time.sleep(10)
            dump_always()
            done_btn = vc.findViewById("com.android.packageinstaller:id/done_button")
            if done_btn:
                done_btn.touch()
                time.sleep(5)

    prefix, switch = switch_arch()
    run_test(prefix=prefix)
    if switch:
        dump_always()
        return_btn = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/v_top_left")
        return_btn.touch()

        time.sleep(2)
        dump_always()
        return_btn = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/v_top_left")
        return_btn.touch()

        time.sleep(2)
        dump_always()
        rating_window = vc.findViewById("com.antutu.ABenchMark:id/rating_title_tv")
        if rating_window:
            not_btn = vc.findViewWithTextOrRaise(u'NOT NOW')
            not_btn.touch()

        prefix, switch = switch_arch()
        run_test(prefix=prefix)


if __name__ == '__main__':
    main()
