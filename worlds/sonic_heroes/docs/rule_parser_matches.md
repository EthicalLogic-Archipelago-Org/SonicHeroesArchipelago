
# Sonic Heroes Archipelago Rule Parser


The rule parser used by this APWorld parses csv files and generates python files from the data. This is to help with performance as file IO is expensive during generation or import. It reads from csv_data folder and outputs to parsed_data folder.

Here is the list of current rules supported by the parser. This can be added to if needed for more rules.

The parser supports ```AND``` and ```OR``` and any amount of nested ```()``` for combining rules to make more complicated complex rules. Note that ```()``` are **REQUIRED** to ensure correct order or operations.

An example rule would be: ```(TripleSpringAND(GlideOR(Homing0ANDTornado0Hover)))ORJumpOR(FlyAnyANDThundershoot0)```


Note that enemies have their own rules both for existing and for being able to be destroyed so do NOT manually write out rules for killing enemies.


===================================================
===================================================

## Character Rules


#### SpeedChar
- Do you have the speed character?
  - The speed character can run up steep slopes by default

#### PowerChar
- Do you have the power character?
  - This is used with other rules as the power character is useless by themselves

#### FlyingChar
- Do you have the flying character?
  - This is used with other rules as the flying character is useless by themselves

#### TallChar
- Do you have the power character and are they tall? (so Omega, Big, or Vector)
  - This is used with other rules

#### FullFlyingStack
- Do you have all 3 characters?
  - Flying formation stacks the characters vertically so having all 3 means the stack is complete

#### FullFlyingStackwithTallChar
- Do you have all 3 characters and a tall character (so Omega, Big, or Vector)?
  - Flying formation stacks the characters vertically so having all 3 means the stack is complete




## Ability Rules (General)


#### BreakThings
- Can you break the Large Cement Blocks in Seaside Hill?
  - This rule is subject to change as I intend to separate each object's break rule.
  - This rule evaluates to: ```PowerAttack0ORBellyFlop0ORFireDunk0ORCombo1```
  - Note that Team Sonic's Team Blast is also capable of this (but as Team Blast requires all abilities, it is not relevant here)

#### BreakWoodContainer
- Can you break the Wooden Containers?
  - Note that inground containers might get a separate rule in the future.
  - This rule evaluates to: ```KickORAccelHalfORPowerAttack0ORBellyFlop0ORFireDunk0ORCombo1```

#### BreakIronContainer
- Can you break the Iron Containers?
  - Note that inground containers might get a separate rule in the future.
  - This rule evaluates to: ```PowerAttack0ORBellyFlop0ORFireDunk0ORCombo1```

#### ComboHeight
- Can you Combo Attack and gain height with it?
  - Knuckles' Combo Finisher gains a small amount of height which can be used to get on top of small ledges.
  - The other power characters do not have this so this is only limited to Knuckles.

#### Jump
- Can you Jump?

#### TeamBlast
- Can you Team Blast?
  - Team Sonic's Team Blast is in fact a Light Attack.
- Team Blast requires All characters and All Abilities for the team (except Jump)


## Ability Rules (Speed Character)
- These rules all require having the speed character


#### Kick
- Can you Kick?
  - Kick is the state where the speed character goes into a ball before preparing to rocket accel.
  - This is possible with only the speed character (unlike rocket accel).
  - This is capable of damaging enemies safely.


#### HammerHover
- Amy has a special move where she hovers by spinning her Piko Hammer rapidly when holding the jump button after jumping.
  - This extends hover frames and allows for gaining extra height.
  - It can also be extended by using tornado and not letting go of the jump button. (though this is a separate rule)
- This rule includes ```Jump``` as a requirement

#### Homing0 Homing1 Homing2 Homing3
- Can you Homing Attack?
  - The number at the end is the required character level. 
  - The range and damage of this ability is increased by character level.
- This rule includes ```Jump``` as a requirement


#### Tornado0 Tornado1 Tornado2 Tornado3
- Can you Tornado?
  - The number at the end is the required character level. 
  - The range of this ability is increased by character level.
  - Be careful to also include the rule for having the enemy spawned if the enemy is required.
- This rule includes ```Jump``` as a requirement



#### AccelHalf AccelFull
- Can you Rocket Accel?
  - Rocket Accel is where the other 2 characters kick the speed character forward while in the spin dash state.
  - This gives a bunch of speed and can activate poles and remove shield just like tornado.
  - Half only requires 1 other character and Full requires both other characters.
- This rule includes ```PowerCharORFlyingChar``` as ```AccelHalf``` and ```PowerCharANDFlyingChar``` as ```AccelFull``` as a requirement



#### LightDash
- Can you Light Dash?
  - Light Dash allows the Speed Character to follow a line of rings exactly, even over bottomless pits.
  - Amy and Espio are not allowed to do this but that may change in a future update.
- This rule includes ```Rings``` as a requirement


#### TriangleJump
- Can you Triangle Jump?
  - Homing Attacking a wall in a hallway will stick to the wall and allow for continued Triangle Jumps in the hallway.
  - Amy is not allowed to do this but that may change in a future update.
- This rule includes ```Homing0``` as a requirement



#### LightAttack
- Can you Light Attack?
  - Sonic has a small time frame after Team Blasting where he can perform a Light Attack by Jumping and pressing the Action button when there is an enemy nearby.
  - This will kill any enemy in the game and severely damage bosses.
- This rule includes ```JumpANDTeamBlast``` as a requirement



#### Invis
- Can you go invisible
  - Espio goes invisible after a tornado.
  - This allows for passing enemies stealthily.
  - I may add this ability to the other speed characters in the future.
- This rule includes ```Tornado0``` as a requirement


#### Shuriken
- Can you throw shurikens?
  - Espio can throw shurikens during Kick.
  - This can be done while invisible and will not break it.



## Ability Rules (Flying Character)
- These rules all require having the flying character


#### FlowerSting
- Can you Flower Sting?
  - Flower Sting is Charmy's special move that can open WarpFlowers.



#### Thundershoot0 Thundershoot1 Thundershoot2 Thundershoot3
- Can you Thundershoot?
  - The number at the end is the required character level. 
  - The range and damage of this ability is increased by character level.
- This rule includes ```SpeedCharORPowerChar``` as a requirement


#### FlyAny FlyOneChar FlyFull
- Can you Fly?
  - ```FlyAny``` does not require any other characters, ```FlyOneChar``` requires 1 other character, and ```FlyingFull``` requires all 3 characters.
  - Generally, you should only need ```FlyAny``` as you can combine it with the Character rules.
  - Flight will **ALWAYS** have Thundershoot unlocked at the same time to prevent softlocks.
- This does **NOT** include any way of getting off the ground so either make sure the player can walk off the platform or include ```Jump``` or ```Thundershoot0``` as a way of getting of the ground.




## Ability Rules (Power Character)
- These rules all require having the power character.

#### PowerAttack0
- Can you Attack with the Power Character?
  - The number at the end is the required character level. 
  - The damage of this ability is increased by character level.

  
#### BellyFlop0
- Can you Belly Flop?
  - The number at the end is the required character level. 
  - The damage of this ability is increased by character level.
  - Belly Flop is limited to Big and Vector.

#### FireDunk0
- Can you Fire Dunk?
  - The number at the end is the required character level. 
  - The damage of this ability is increased by character level.
- This rule includes ```JumpAND(SpeedCharORFlyingChar)``` as a requirement.


#### Combo1
- Can you perform the power character's combo finisher?
  - The number at the end is the required character level. 
  - The combo finisher gains extra functionality and damage with character level.
- This rule includes ```PowerAttack0``` as a requirement.




## Enemy Rules
- These rules involve enemies (both spawning them and destroying them)
- Kill enemy rules require specifying the weapons/shields/armor/special type of the enemy and the height. (ground enemy rules default to ground height unless specified)
- All Kill rules also include the spawn rule as a requirement.


#### RedFlapper
- Are Red Flappers with No Weapon and No Armor spawned?
  - This can be combined with ```Homing0``` for homing attack chains.


#### KillRedFlapperGround KillRedFlapperHalfJump KillRedFlapperJump
- Can you destroy Red Flappers with No Weapon and No Armor at the specified height?



#### GreenFlapperBazooka
- Are Green Flappers with Bazookas and No Armor spawned?


#### KillGreenFlapperBazookaHalfJump KillGreenFlapperBazookaJump KillGreenFlapperBazookaTallCharJump
- Can you destroy Green Flappers with Bazookas and No Armor at the specified height?



#### KillGreenFlapperBazookaJumpHomingOnly
- Can you destroy Green Flappers with Bazookas and No Armor at Jump height with homing attack only?
  - This is used to logic out using homing attack to reach a higher up red flapper .

  

#### EggPawnNothing
- Are Egg Pawns with No Weapon and No Shield spawned?
  - I may in the future separate Casino Pawns or King Pawns.


#### KillEggPawnNothing KillEggPawnNothingJump
- Can you destroy Egg Pawns with No Weapon and No Shield at the specified height? (default is Ground)


#### KillEggPawnNothingBobsled
- Can you destroy Egg Pawns with No Weapon and No Shield that are in a bobsled's path?
  - This has ```BobsledAnyAND(SpeedCharORPowerChar)``` as a requirement. (in addition to ```EggPawnNothing```)


#### KillEggPawnNothingSHFirstBobsled
- Can you destroy Egg Pawns with No Weapon and No Shield that are in Seaside Hill's first bobsled's path with specifically the bobsled? (and only the bobsled)
  - I am undecided if I will continue to remove the first SH bobsled so this rule will handle that. 
  - This currently evaluates to ```False``` but that may change in the future.
  - If you are routing one of these enemies on not Chaotix (as Chaotix removes that bobsled in vanilla), do ```KillEggPawnNothingORKillEggPawnNothingSHFirstBobsled``` for now.


#### EggPawnBazooka
- Are Egg Pawns with Bazooka and No Shield spawned?
  - I may in the future separate Casino Pawns or King Pawns.


#### KillEggPawnBazooka
- Can you destroy Egg Pawns with Bazooka and No Shield at the specified height? (default is Ground)


#### EggPawnLance
- Are Egg Pawns with Lance and No Shield spawned?
  - I may in the future separate Casino Pawns or King Pawns.


#### KillEggPawnLance
- Can you destroy Egg Pawns with Lance and No Shield at the specified height? (default is Ground)


#### EggPawnLanceConcreteShield
- Are Egg Pawns with Lance and Concrete Shield spawned?
  - I may in the future separate Casino Pawns or King Pawns.


#### KillEggPawnLanceConcreteShield
- Can you destroy Egg Pawns with Lance and Concrete Shield at the specified height? (default is Ground)




## Stage Object Rules
- These rules involve Stage Objects (Bobsled is not a Stage Object but is here anyway)


#### BobsledAny
- Are Bobsleighs Spawned?
  - This only wants a single character and does not care which character that is.
  - So care must be taken if the specific location requires a certain bobsled character.



#### SingleSpring

#### TripleSpring

#### Rings

#### HintRing

#### DashRamp

#### DashPanel

#### DashRing

#### RainbowHoop

#### Cannon

#### ItemBox

#### ItemBalloon

#### GoalRing

#### WarpFlower



#### RuinsNoTrigger
- Are Moving Ruins Spawned?
  - This does not check for the Trigger Ruins Object so use this for ruins that do not move.


#### RuinsTrigger
- Are Moving Ruins and Triggers Spawned?
  - This checks for the Trigger Ruins Object so use this for ruins that move or have a linked Trigger.




## Trick Rules
- These rules involve tricks.



#### Medium
- This marks the specific rule as harder than wanted for base logic,
  - I may add more difficulties in the future but for specific tricks, I want them marked as their trick rule. (to avoid having a large opaque difficulty choice)
  - This currently is used for more difficult jumps that don't fit into other trick rules.


#### BadnikBounce
- Can you jump into an enemy to gain extra height from a normal jump?
  - Make sure to include Jump and the enemy rule as well.



#### CollisAbuse
- This is a catch-all for abusing collision in unintended ways.
  - For example, jumping into a slanted wall can gain unexpected height.


#### HoverFrame
- Holding the Jump button for longer during the jump can extend the game's "hover frames".
  - This specific trick is limited without other abilities to improve the height gain.


#### Homing0Hover
- Combining Hover Frames with Homing Attack can allow for reaching some higher enemies than expected.
- This has ```Homing0``` as a requirement.



#### Tornado0Hover
- Combining Hover Frames with Tornado (specifically Sonic's and Shadow's Tornado) can allow for significant height gain.
  - Care must be taken (if enemies are present and the lock on feature is not intended) to include the kill enemy rule to prevent softlocks.
  - I may in the future allow Amy and Espio to have the default tornado.
- This has ```Tornado0``` as a requirement.



#### Parkour
- This is used to mark dangerous platforming (but not necessarily difficult).
  - For example, staying on top of the white edges of the Seaside Hill paths would fit here.




#### FlyDepleteBoost
- Gaining height during a flight at the same time the flight meter runs out can gain height above the cap.
  - The timing of this one is fairly precise.
- This has ```FlyAny``` as a requirement. (so make sure to include ```Thundershoot0``` or ```Jump``` if needed)


#### FlyGroundBounce
- Jumping near the same frame as touching the ground while in flight mode can both gain high above a regular jump and end flight mode. (to allow you to start it again)
  - By starting another flight at the top of this "jump", you gain a significant amount of extra height.
  - The timing of this is substantially harder without having Jump so this rule has 2 parts.
- This rule specifically allows for walking off of the ground to start flight. (see ```FlyGroundBounceThundershoot``` for if that is not possible)
- This rule handles both Having Jump with the easier YAML option and not having Jump with the harder YAML option.
- This has ```FlyAny``` as a requirement. (```Jump``` is a requirement for the easier handling so it is not needed to be included)


#### FlyGroundBounceThundershoot
- This is ```FlyGroundBounce``` but with the caveat of requiring Thundershoot if Jump is not possible.
- This rule handles both Having Jump with the easier YAML option and not having Jump with the harder YAML option.
- This has ```FlyAny``` as a requirement. (```Jump``` is a requirement for the easier handling and ```Thundershoot0``` is a requirement for the harder handling so it is not needed to be included)


