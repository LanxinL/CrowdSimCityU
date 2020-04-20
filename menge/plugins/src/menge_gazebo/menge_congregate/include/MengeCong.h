/*
 * MengePlugin.h
 *
 *  Created on: Jul 2, 2016
 *      Author: Michael Huang
 */

#ifndef MENGECONG_H_
#define MENGECONG_H_
#include "MengePlugin.h"
namespace gazebo {

class MengeCong:public MengePlugin {

protected:

	virtual void insertAgentModel(const Menge::Agents::BaseAgent* agt);
	virtual void insertAgentActor(const Menge::Agents::BaseAgent* agt);

};
GZ_REGISTER_WORLD_PLUGIN(MengeCong)
} /* namespace gazebo */

#endif /* MENGEPLUGIN_H_ */
