import React, { ChangeEvent } from 'react';
import { gameService } from '../../services';
import { AppStateContainer, MapStateContainer } from '../../models';
import { Checkbox, FormControlLabel } from '@mui/material';

export function AdminMenuBar() {
  const { commanderMode, setCommanderMode, setShowLoadMissionForm, setShowSaveAsMissionForm } =
    AppStateContainer.useContainer();
  const { showAllGroups, setShowAllGroups } = MapStateContainer.useContainer();

  const saveOnClick = () => {
    console.log('Saving mission.');
    gameService.sendSaveMission();
  };

  const loadOnClick = () => {
    setShowLoadMissionForm(true);
  };

  const downloadOnClick = () => {
    console.log('Downloading mission.');
    // Create a temporary link to trigger the download
    const link = document.createElement('a');
    link.href = '/game/download_mission';
    link.download = 'mission.miz';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const onShowAllGroupsChange = (event: ChangeEvent, checked: boolean) => setShowAllGroups(checked);
  const onCommanderModeChange = (event: ChangeEvent, checked: boolean) => setCommanderMode(checked);

  return (
    <React.Fragment>
      <button onClick={loadOnClick}>Load</button>
      <button onClick={saveOnClick}>Save</button>
      <button onClick={downloadOnClick}>Download</button>
      <button onClick={() => setShowSaveAsMissionForm(true)}>Save as</button>
      <FormControlLabel
        value="start"
        control={<Checkbox checked={showAllGroups} color="primary" onChange={onShowAllGroupsChange} />}
        label="Show all groups"
        labelPlacement="end"
      />
      <FormControlLabel
        value="start"
        control={<Checkbox checked={commanderMode} color="secondary" onChange={onCommanderModeChange} />}
        label="Commander Mode"
        labelPlacement="end"
      />
    </React.Fragment>
  );
}
